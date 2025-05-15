#!/usr/bin/env python3
"""
Service Analyzer for grimOS

This script analyzes the grimOS microservices architecture,
identifying services, their dependencies, and communication patterns.

Usage:
    python service_analyzer.py [--index INDEX_FILE] [--output OUTPUT_FILE]

Author: grimOS Team
"""

import os
import json
import re
import argparse
from typing import Dict, List, Any, Optional, Set, Tuple


class ServiceAnalyzer:
    """
    Analyzes the grimOS microservices architecture.
    
    This class identifies services, their dependencies, and communication patterns
    between services in the grimOS workspace.
    """
    
    def __init__(self, index_path: str = "workspace_index.json"):
        """
        Initialize the service analyzer.
        
        Args:
            index_path: Path to the workspace index file
        """
        self.index_path = index_path
        self.index = self._load_index()
        self.services = {}
        self.dependencies = {}
        self.communication_patterns = {}
        
    def _load_index(self) -> Dict[str, Any]:
        """
        Load the workspace index.
        
        Returns:
            Dict containing the workspace index
        """
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file not found: {self.index_path}")
            
        with open(self.index_path, 'r') as f:
            return json.load(f)
    
    def _detect_services(self) -> None:
        """
        Detect microservices in the workspace.
        """
        # Reset services
        self.services = {}
        
        # Check for services in the services directory
        for dir_path in self.index.get("directories", []):
            # Microservices in services directory
            if dir_path.startswith("services/") and dir_path.count("/") == 1:
                service_name = dir_path.split("/")[1]
                self.services[service_name] = {
                    "name": service_name,
                    "path": dir_path,
                    "type": "microservice",
                    "files": [],
                    "endpoints": [],
                    "dependencies": [],
                    "communication": {
                        "kafka": [],
                        "grpc": [],
                        "rest": []
                    }
                }
            # Backend services in apps directory
            elif dir_path.startswith("apps/backend/") and dir_path.count("/") == 2:
                service_name = dir_path.split("/")[2]
                self.services[service_name] = {
                    "name": service_name,
                    "path": dir_path,
                    "type": "backend",
                    "files": [],
                    "endpoints": [],
                    "dependencies": [],
                    "communication": {
                        "kafka": [],
                        "grpc": [],
                        "rest": []
                    }
                }
            # Frontend services in apps directory
            elif dir_path.startswith("apps/frontend/") and dir_path.count("/") == 2:
                service_name = dir_path.split("/")[2]
                self.services[service_name] = {
                    "name": service_name,
                    "path": dir_path,
                    "type": "frontend",
                    "files": [],
                    "endpoints": [],
                    "dependencies": [],
                    "communication": {
                        "api": []
                    }
                }
        
        # Assign files to services
        for file_info in self.index.get("files", []):
            file_path = file_info.get("path", "")
            
            for service_name, service_info in self.services.items():
                service_path = service_info["path"]
                if file_path.startswith(service_path + "/"):
                    self.services[service_name]["files"].append(file_path)
                    break
    
    def _analyze_dependencies(self) -> None:
        """
        Analyze dependencies between services.
        """
        # Reset dependencies
        for service_name in self.services:
            self.services[service_name]["dependencies"] = []
        
        # Check Python requirements files
        for service_name, service_info in self.services.items():
            requirements_files = [
                f for f in service_info["files"] 
                if f.endswith("requirements.txt") or f.endswith("pyproject.toml")
            ]
            
            for req_file in requirements_files:
                if req_file in [f["path"] for f in self.index.get("files", []) if "content" in f]:
                    # Get file content from index if available
                    content = next(f["content"] for f in self.index.get("files", []) 
                                  if f["path"] == req_file and "content" in f)
                    
                    # Parse dependencies
                    if req_file.endswith("requirements.txt"):
                        for line in content.splitlines():
                            line = line.strip()
                            if line and not line.startswith("#"):
                                # Extract package name
                                package = line.split("==")[0].split(">=")[0].split(">")[0].strip()
                                self.services[service_name]["dependencies"].append({
                                    "name": package,
                                    "type": "python",
                                    "source": req_file
                                })
                    elif req_file.endswith("pyproject.toml"):
                        # Simple TOML parsing for dependencies
                        in_dependencies = False
                        for line in content.splitlines():
                            line = line.strip()
                            if line == "[tool.poetry.dependencies]" or line == "[project.dependencies]":
                                in_dependencies = True
                            elif line.startswith("[") and line.endswith("]"):
                                in_dependencies = False
                            elif in_dependencies and "=" in line:
                                package = line.split("=")[0].strip()
                                self.services[service_name]["dependencies"].append({
                                    "name": package,
                                    "type": "python",
                                    "source": req_file
                                })
        
        # Check JavaScript package.json files
        for service_name, service_info in self.services.items():
            package_files = [f for f in service_info["files"] if f.endswith("package.json")]
            
            for pkg_file in package_files:
                if pkg_file in [f["path"] for f in self.index.get("files", []) if "content" in f]:
                    # Get file content from index if available
                    content = next(f["content"] for f in self.index.get("files", []) 
                                  if f["path"] == pkg_file and "content" in f)
                    
                    try:
                        # Parse JSON
                        package_data = json.loads(content)
                        
                        # Extract dependencies
                        for dep_type in ["dependencies", "devDependencies"]:
                            if dep_type in package_data:
                                for pkg_name in package_data[dep_type]:
                                    self.services[service_name]["dependencies"].append({
                                        "name": pkg_name,
                                        "type": "javascript",
                                        "dev": dep_type == "devDependencies",
                                        "source": pkg_file
                                    })
                    except json.JSONDecodeError:
                        print(f"Error parsing JSON in {pkg_file}")
    
    def _analyze_communication(self) -> None:
        """
        Analyze communication patterns between services.
        """
        # Reset communication patterns
        self.communication_patterns = {}
        
        # Analyze Kafka communication
        self._analyze_kafka_communication()
        
        # Analyze gRPC communication
        self._analyze_grpc_communication()
        
        # Analyze REST API communication
        self._analyze_rest_communication()
    
    def _analyze_kafka_communication(self) -> None:
        """
        Analyze Kafka communication patterns.
        """
        kafka_pattern = re.compile(r'(kafka|KafkaProducer|KafkaConsumer|send_message|consume_message)')
        topic_pattern = re.compile(r'topic\s*=\s*[\'"]([^\'"]+)[\'"]')
        
        for service_name, service_info in self.services.items():
            for file_path in service_info["files"]:
                if file_path.endswith(".py") or file_path.endswith(".ts") or file_path.endswith(".js"):
                    # Check if file content is available in index
                    file_content = None
                    for f in self.index.get("files", []):
                        if f["path"] == file_path and "content" in f:
                            file_content = f["content"]
                            break
                    
                    if file_content and kafka_pattern.search(file_content):
                        # Found Kafka usage
                        topics = topic_pattern.findall(file_content)
                        
                        for topic in topics:
                            kafka_info = {
                                "topic": topic,
                                "file": file_path
                            }
                            
                            # Determine if producer or consumer
                            if "Producer" in file_content or "send_message" in file_content:
                                kafka_info["role"] = "producer"
                                self.services[service_name]["communication"]["kafka"].append(kafka_info)
                            
                            if "Consumer" in file_content or "consume_message" in file_content:
                                kafka_info["role"] = "consumer"
                                self.services[service_name]["communication"]["kafka"].append(kafka_info)
    
    def _analyze_grpc_communication(self) -> None:
        """
        Analyze gRPC communication patterns.
        """
        grpc_pattern = re.compile(r'(grpc|GRPC|protobuf|Stub)')
        
        for service_name, service_info in self.services.items():
            # Check for .proto files
            proto_files = [f for f in service_info["files"] if f.endswith(".proto")]
            
            for proto_file in proto_files:
                # Service is using gRPC
                self.services[service_name]["communication"]["grpc"].append({
                    "proto_file": proto_file,
                    "role": "definition"
                })
            
            # Check for gRPC client/server code
            for file_path in service_info["files"]:
                if file_path.endswith(".py") or file_path.endswith(".ts") or file_path.endswith(".js"):
                    # Check if file content is available in index
                    file_content = None
                    for f in self.index.get("files", []):
                        if f["path"] == file_path and "content" in f:
                            file_content = f["content"]
                            break
                    
                    if file_content and grpc_pattern.search(file_content):
                        # Found gRPC usage
                        if "server" in file_path.lower() or "Server" in file_content:
                            self.services[service_name]["communication"]["grpc"].append({
                                "file": file_path,
                                "role": "server"
                            })
                        
                        if "client" in file_path.lower() or "Client" in file_content or "Stub" in file_content:
                            self.services[service_name]["communication"]["grpc"].append({
                                "file": file_path,
                                "role": "client"
                            })
    
    def _analyze_rest_communication(self) -> None:
        """
        Analyze REST API communication patterns.
        """
        rest_pattern = re.compile(r'(@app\.(get|post|put|delete)|router\.(get|post|put|delete)|axios\.(get|post|put|delete)|fetch\(|httpx\.(get|post|put|delete)|requests\.(get|post|put|delete))')
        
        for service_name, service_info in self.services.items():
            for file_path in service_info["files"]:
                if file_path.endswith(".py") or file_path.endswith(".ts") or file_path.endswith(".js"):
                    # Check if file content is available in index
                    file_content = None
                    for f in self.index.get("files", []):
                        if f["path"] == file_path and "content" in f:
                            file_content = f["content"]
                            break
                    
                    if file_content and rest_pattern.search(file_content):
                        # Found REST API usage
                        if "@app." in file_content or "router." in file_content or "app.add_api_route" in file_content:
                            # Server/endpoint
                            self.services[service_name]["communication"]["rest"].append({
                                "file": file_path,
                                "role": "server"
                            })
                            
                            # Extract endpoints
                            endpoint_pattern = re.compile(r'@app\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]')
                            router_pattern = re.compile(r'router\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]')
                            fastapi_pattern = re.compile(r'app\.add_api_route\([\'"]([^\'"]+)[\'"].*,\s*methods=\[[\'"](GET|POST|PUT|DELETE)[\'"]')
                            
                            for method, path in endpoint_pattern.findall(file_content):
                                self.services[service_name]["endpoints"].append({
                                    "method": method.upper(),
                                    "path": path,
                                    "file": file_path
                                })
                                
                            for method, path in router_pattern.findall(file_content):
                                self.services[service_name]["endpoints"].append({
                                    "method": method.upper(),
                                    "path": path,
                                    "file": file_path
                                })
                                
                            for path, method in fastapi_pattern.findall(file_content):
                                self.services[service_name]["endpoints"].append({
                                    "method": method,
                                    "path": path,
                                    "file": file_path
                                })
                        
                        if "axios." in file_content or "fetch(" in file_content or "httpx." in file_content or "requests." in file_content:
                            # Client
                            self.services[service_name]["communication"]["rest"].append({
                                "file": file_path,
                                "role": "client"
                            })
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the workspace services.
        
        Returns:
            Dict containing analysis results
        """
        # Detect services
        self._detect_services()
        
        # Analyze dependencies
        self._analyze_dependencies()
        
        # Analyze communication patterns
        self._analyze_communication()
        
        # Build service graph
        service_graph = self._build_service_graph()
        
        # Prepare results
        results = {
            "services": self.services,
            "service_count": len(self.services),
            "service_graph": service_graph,
            "analysis_timestamp": self.index.get("indexed_at", "")
        }
        
        return results
    
    def _build_service_graph(self) -> Dict[str, Any]:
        """
        Build a graph of service relationships.
        
        Returns:
            Dict containing the service graph
        """
        graph = {
            "nodes": [],
            "edges": []
        }
        
        # Add nodes for each service
        for service_name, service_info in self.services.items():
            graph["nodes"].append({
                "id": service_name,
                "label": service_name,
                "type": service_info["type"]
            })
        
        # Add edges for Kafka communication
        for source_service, source_info in self.services.items():
            for kafka_info in source_info["communication"]["kafka"]:
                if kafka_info.get("role") == "producer":
                    topic = kafka_info.get("topic")
                    
                    # Find consumers of this topic
                    for target_service, target_info in self.services.items():
                        if source_service != target_service:
                            for target_kafka in target_info["communication"]["kafka"]:
                                if (target_kafka.get("role") == "consumer" and 
                                    target_kafka.get("topic") == topic):
                                    graph["edges"].append({
                                        "source": source_service,
                                        "target": target_service,
                                        "type": "kafka",
                                        "label": f"Kafka: {topic}"
                                    })
        
        # Add edges for gRPC communication
        for source_service, source_info in self.services.items():
            for grpc_info in source_info["communication"]["grpc"]:
                if grpc_info.get("role") == "server":
                    # Find clients
                    for target_service, target_info in self.services.items():
                        if source_service != target_service:
                            for target_grpc in target_info["communication"]["grpc"]:
                                if target_grpc.get("role") == "client":
                                    graph["edges"].append({
                                        "source": target_service,
                                        "target": source_service,
                                        "type": "grpc",
                                        "label": "gRPC"
                                    })
        
        # Add edges for REST communication
        for source_service, source_info in self.services.items():
            for rest_info in source_info["communication"]["rest"]:
                if rest_info.get("role") == "server":
                    # Find clients
                    for target_service, target_info in self.services.items():
                        if source_service != target_service:
                            for target_rest in target_info["communication"]["rest"]:
                                if target_rest.get("role") == "client":
                                    graph["edges"].append({
                                        "source": target_service,
                                        "target": source_service,
                                        "type": "rest",
                                        "label": "REST"
                                    })
        
        return graph
    
    def save_analysis(self, output_path: str = "service_analysis.json") -> None:
        """
        Save the analysis results to a file.
        
        Args:
            output_path: Path to save the analysis results
        """
        results = self.analyze()
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"Service analysis saved to {output_path}")
        print(f"Analyzed {results['service_count']} services")


def main():
    """Main entry point for the service analyzer."""
    parser = argparse.ArgumentParser(description='grimOS Service Analyzer')
    parser.add_argument('--index', default='workspace_index.json', help='Path to workspace index file')
    parser.add_argument('--output', default='service_analysis.json', help='Output file path')
    
    args = parser.parse_args()
    
    try:
        analyzer = ServiceAnalyzer(args.index)
        analyzer.save_analysis(args.output)
        return 0
    except Exception as e:
        print(f"Error analyzing services: {e}")
        return 1


if __name__ == "__main__":
    exit(main())