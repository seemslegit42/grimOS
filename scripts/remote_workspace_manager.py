#!/usr/bin/env python3
"""
Remote Workspace Manager for grimOS

This script orchestrates the workspace indexing, analysis, and visualization
processes for the grimOS project, enabling remote development and collaboration.

Usage:
    python remote_workspace_manager.py [--config CONFIG_FILE] [--index] [--analyze] [--visualize] [--sync]

Author: grimOS Team
"""

import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional


class RemoteWorkspaceManager:
    """
    Manages the grimOS remote workspace.
    
    This class orchestrates the workspace indexing, analysis, and visualization
    processes, enabling remote development and collaboration.
    """
    
    def __init__(self, config_path: str = "scripts/workspace_config.json"):
        """
        Initialize the remote workspace manager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.root_dir = os.getcwd()
        self.index_file = self.config.get("indexFile", "workspace_index.json")
        self.service_analysis_file = "service_analysis.json"
        self.visualization_file = "workspace_visualization.html"
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Load the workspace configuration.
        
        Returns:
            Dict containing the configuration
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def build_index(self) -> bool:
        """
        Build the workspace index.
        
        Returns:
            True if successful, False otherwise
        """
        print("Building workspace index...")
        start_time = time.time()
        
        try:
            # Run the workspace indexer
            result = subprocess.run(
                [sys.executable, "scripts/workspace_indexer.py", "--config", self.config_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout)
                print(f"Workspace index built successfully in {time.time() - start_time:.2f} seconds")
                return True
            else:
                print(f"Error building workspace index: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error building workspace index: {e}")
            return False
    
    def analyze_services(self) -> bool:
        """
        Analyze the workspace services.
        
        Returns:
            True if successful, False otherwise
        """
        print("Analyzing services...")
        start_time = time.time()
        
        try:
            # Run the service analyzer
            result = subprocess.run(
                [sys.executable, "scripts/service_analyzer.py", "--index", self.index_file, "--output", self.service_analysis_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout)
                print(f"Service analysis completed successfully in {time.time() - start_time:.2f} seconds")
                return True
            else:
                print(f"Error analyzing services: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error analyzing services: {e}")
            return False
    
    def generate_visualization(self) -> bool:
        """
        Generate the workspace visualization.
        
        Returns:
            True if successful, False otherwise
        """
        print("Generating visualization...")
        start_time = time.time()
        
        try:
            # Run the workspace visualizer
            result = subprocess.run(
                [sys.executable, "scripts/workspace_visualizer.py", "--index", self.index_file, "--config", self.config_path, "--output", self.visualization_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout)
                print(f"Visualization generated successfully in {time.time() - start_time:.2f} seconds")
                return True
            else:
                print(f"Error generating visualization: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error generating visualization: {e}")
            return False
    
    def sync_to_remote(self) -> bool:
        """
        Sync the workspace to a remote location.
        
        Returns:
            True if successful, False otherwise
        """
        print("Syncing to remote...")
        start_time = time.time()
        
        try:
            # Run the workspace indexer with sync option
            result = subprocess.run(
                [sys.executable, "scripts/workspace_indexer.py", "--config", self.config_path, "--sync"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout)
                print(f"Remote sync completed successfully in {time.time() - start_time:.2f} seconds")
                return True
            else:
                print(f"Error syncing to remote: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error syncing to remote: {e}")
            return False
    
    def run_all(self) -> bool:
        """
        Run all workspace management tasks.
        
        Returns:
            True if all tasks were successful, False otherwise
        """
        print(f"=== grimOS Remote Workspace Manager ===")
        print(f"Started at: {datetime.now().isoformat()}")
        print(f"Project: {self.config.get('projectName', 'grimOS')}")
        print(f"Root directory: {self.root_dir}")
        print("=" * 40)
        
        success = True
        
        # Build index
        if not self.build_index():
            success = False
        
        # Analyze services
        if success and not self.analyze_services():
            success = False
        
        # Generate visualization
        if success and not self.generate_visualization():
            success = False
        
        # Sync to remote
        if success and self.config.get("remoteSync", {}).get("enabled", False):
            if not self.sync_to_remote():
                success = False
        
        print("=" * 40)
        print(f"Completed at: {datetime.now().isoformat()}")
        print(f"Status: {'Success' if success else 'Failed'}")
        
        return success


def main():
    """Main entry point for the remote workspace manager."""
    parser = argparse.ArgumentParser(description='grimOS Remote Workspace Manager')
    parser.add_argument('--config', default='scripts/workspace_config.json', help='Configuration file path')
    parser.add_argument('--index', action='store_true', help='Build workspace index')
    parser.add_argument('--analyze', action='store_true', help='Analyze services')
    parser.add_argument('--visualize', action='store_true', help='Generate visualization')
    parser.add_argument('--sync', action='store_true', help='Sync to remote')
    parser.add_argument('--all', action='store_true', help='Run all tasks')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = RemoteWorkspaceManager(args.config)
    
    # Determine which tasks to run
    run_all = args.all or not (args.index or args.analyze or args.visualize or args.sync)
    
    if run_all:
        success = manager.run_all()
    else:
        success = True
        
        if args.index:
            success = manager.build_index() and success
        
        if args.analyze:
            success = manager.analyze_services() and success
        
        if args.visualize:
            success = manager.generate_visualization() and success
        
        if args.sync:
            success = manager.sync_to_remote() and success
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())