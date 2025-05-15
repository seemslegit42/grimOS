#!/usr/bin/env python3
"""
Workspace Visualizer for grimOS

This script generates visualizations of the grimOS workspace structure
based on the workspace index created by workspace_indexer.py.

Usage:
    python workspace_visualizer.py [--index INDEX_FILE] [--output OUTPUT_FILE]

Author: grimOS Team
"""

import os
import json
import argparse
from typing import Dict, List, Any, Optional, Set, Tuple


class WorkspaceVisualizer:
    """
    Generates visualizations of the grimOS workspace structure.
    
    This class creates HTML visualizations of the workspace structure,
    including file relationships, directory structure, and service dependencies.
    """
    
    def __init__(self, index_path: str = "workspace_index.json", config_path: str = "scripts/workspace_config.json"):
        """
        Initialize the workspace visualizer.
        
        Args:
            index_path: Path to the workspace index file
            config_path: Path to the configuration file
        """
        self.index_path = index_path
        self.config_path = config_path
        self.index = self._load_index()
        self.config = self._load_config()
        
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
    
    def _generate_directory_tree(self) -> str:
        """
        Generate HTML for the directory tree visualization.
        
        Returns:
            HTML string for the directory tree
        """
        # Build directory tree structure
        tree = {}
        for dir_path in self.index.get("directories", []):
            parts = dir_path.split(os.sep)
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        # Generate HTML for the tree
        def build_tree_html(node, path="", level=0):
            html = ""
            for name, children in sorted(node.items()):
                current_path = os.path.join(path, name) if path else name
                html += f'<div class="tree-item" style="margin-left: {level * 20}px">'
                html += f'<span class="tree-folder" onclick="toggleFolder(this)">{name}/</span>'
                html += f'<div class="tree-children">'
                html += build_tree_html(children, current_path, level + 1)
                
                # Add files in this directory
                files_in_dir = [f for f in self.index.get("files", []) 
                               if os.path.dirname(f["path"]) == current_path]
                
                for file_info in sorted(files_in_dir, key=lambda x: x["path"]):
                    file_name = os.path.basename(file_info["path"])
                    file_type = file_info.get("type", "unknown")
                    file_size = file_info.get("size", 0)
                    size_str = f"{file_size / 1024:.1f} KB" if file_size >= 1024 else f"{file_size} bytes"
                    
                    html += f'<div class="tree-file" style="margin-left: {(level + 1) * 20}px">'
                    html += f'<span class="file-type-{file_type}">{file_name}</span>'
                    html += f'<span class="file-size">{size_str}</span>'
                    html += '</div>'
                
                html += '</div></div>'
            return html
        
        return build_tree_html(tree)
    
    def _generate_file_type_chart(self) -> str:
        """
        Generate HTML for the file type chart.
        
        Returns:
            HTML string for the file type chart
        """
        file_types = self.index.get("file_types", {})
        if not file_types:
            return "<p>No file type data available</p>"
            
        # Generate data for chart
        labels = list(file_types.keys())
        values = list(file_types.values())
        
        # Generate colors
        colors = [
            "#4285F4",  # Blue
            "#EA4335",  # Red
            "#FBBC05",  # Yellow
            "#34A853",  # Green
            "#FF6D01",  # Orange
            "#46BDC6",  # Teal
            "#7B1FA2",  # Purple
            "#795548",  # Brown
            "#9E9E9E",  # Grey
            "#607D8B"   # Blue Grey
        ]
        
        # Ensure we have enough colors
        while len(colors) < len(labels):
            colors.extend(colors[:len(labels) - len(colors)])
            
        # Generate HTML and JavaScript for chart
        html = """
        <div class="chart-container">
            <canvas id="fileTypeChart"></canvas>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const ctx = document.getElementById('fileTypeChart').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: %s,
                        datasets: [{
                            data: %s,
                            backgroundColor: %s
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'right',
                            },
                            title: {
                                display: true,
                                text: 'File Types Distribution'
                            }
                        }
                    }
                });
            });
        </script>
        """ % (json.dumps(labels), json.dumps(values), json.dumps(colors))
        
        return html
    
    def _generate_file_extension_chart(self) -> str:
        """
        Generate HTML for the file extension chart.
        
        Returns:
            HTML string for the file extension chart
        """
        file_extensions = self.index.get("file_extensions", {})
        if not file_extensions:
            return "<p>No file extension data available</p>"
            
        # Sort by count and take top 15
        sorted_extensions = sorted(file_extensions.items(), key=lambda x: x[1], reverse=True)[:15]
        labels = [ext for ext, _ in sorted_extensions]
        values = [count for _, count in sorted_extensions]
        
        # Generate HTML and JavaScript for chart
        html = """
        <div class="chart-container">
            <canvas id="fileExtensionChart"></canvas>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const ctx = document.getElementById('fileExtensionChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: %s,
                        datasets: [{
                            label: 'File Count',
                            data: %s,
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: 'Top File Extensions'
                            }
                        }
                    }
                });
            });
        </script>
        """ % (json.dumps(labels), json.dumps(values))
        
        return html
    
    def _generate_changes_section(self) -> str:
        """
        Generate HTML for the changes section.
        
        Returns:
            HTML string for the changes section
        """
        changes = self.index.get("changes", {})
        if not changes:
            return "<p>No change tracking data available</p>"
            
        added = changes.get("added", [])
        modified = changes.get("modified", [])
        deleted = changes.get("deleted", [])
        
        html = "<div class='changes-container'>"
        
        # Added files
        html += "<div class='changes-section'>"
        html += "<h3>Added Files</h3>"
        if added:
            html += "<ul class='changes-list added'>"
            for path in sorted(added):
                html += f"<li>{path}</li>"
            html += "</ul>"
        else:
            html += "<p>No files added</p>"
        html += "</div>"
        
        # Modified files
        html += "<div class='changes-section'>"
        html += "<h3>Modified Files</h3>"
        if modified:
            html += "<ul class='changes-list modified'>"
            for path in sorted(modified):
                html += f"<li>{path}</li>"
            html += "</ul>"
        else:
            html += "<p>No files modified</p>"
        html += "</div>"
        
        # Deleted files
        html += "<div class='changes-section'>"
        html += "<h3>Deleted Files</h3>"
        if deleted:
            html += "<ul class='changes-list deleted'>"
            for path in sorted(deleted):
                html += f"<li>{path}</li>"
            html += "</ul>"
        else:
            html += "<p>No files deleted</p>"
        html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_services_section(self) -> str:
        """
        Generate HTML for the services section.
        
        Returns:
            HTML string for the services section
        """
        # Detect services based on directory structure
        services = []
        
        # Check for services directory
        for dir_path in self.index.get("directories", []):
            if dir_path.startswith("services/") and dir_path.count("/") == 1:
                service_name = dir_path.split("/")[1]
                services.append({
                    "name": service_name,
                    "path": dir_path,
                    "type": "microservice"
                })
            elif dir_path.startswith("apps/backend/") and dir_path.count("/") == 2:
                service_name = dir_path.split("/")[2]
                services.append({
                    "name": service_name,
                    "path": dir_path,
                    "type": "backend"
                })
            elif dir_path.startswith("apps/frontend/") and dir_path.count("/") == 2:
                service_name = dir_path.split("/")[2]
                services.append({
                    "name": service_name,
                    "path": dir_path,
                    "type": "frontend"
                })
        
        if not services:
            return "<p>No services detected</p>"
            
        html = "<div class='services-container'>"
        html += "<h3>Detected Services</h3>"
        html += "<div class='services-grid'>"
        
        for service in sorted(services, key=lambda x: x["name"]):
            service_type = service["type"]
            service_name = service["name"]
            service_path = service["path"]
            
            html += f"<div class='service-card service-{service_type}'>"
            html += f"<div class='service-header'>{service_name}</div>"
            html += f"<div class='service-type'>{service_type}</div>"
            html += f"<div class='service-path'>{service_path}</div>"
            html += "</div>"
        
        html += "</div></div>"
        return html
    
    def generate_html(self, output_path: str = "workspace_visualization.html") -> None:
        """
        Generate HTML visualization of the workspace.
        
        Args:
            output_path: Path to save the HTML file
        """
        # Generate components
        directory_tree = self._generate_directory_tree()
        file_type_chart = self._generate_file_type_chart()
        file_extension_chart = self._generate_file_extension_chart()
        changes_section = self._generate_changes_section()
        services_section = self._generate_services_section()
        
        # Project summary
        project_name = self.index.get("project", "Unknown Project")
        indexed_at = self.index.get("indexed_at", "Unknown")
        file_count = self.index.get("file_count", 0)
        directory_count = self.index.get("directory_count", 0)
        total_size = self.index.get("total_size", 0)
        total_size_mb = total_size / (1024 * 1024)
        
        # Generate full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} Workspace Visualization</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary-color: #4285F4;
            --secondary-color: #34A853;
            --accent-color: #EA4335;
            --background-color: #f9f9f9;
            --card-background: #ffffff;
            --text-color: #333333;
            --border-color: #e0e0e0;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background-color: var(--primary-color);
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 5px;
        }}
        
        h1, h2, h3 {{
            margin-top: 0;
        }}
        
        .card {{
            background-color: var(--card-background);
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-item {{
            background-color: var(--card-background);
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
        }}
        
        .summary-value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary-color);
            margin: 10px 0;
        }}
        
        .summary-label {{
            font-size: 0.9rem;
            color: #666;
        }}
        
        .chart-container {{
            height: 400px;
            margin-bottom: 30px;
        }}
        
        .tree-item {{
            margin-bottom: 5px;
        }}
        
        .tree-folder {{
            cursor: pointer;
            font-weight: bold;
            color: var(--primary-color);
        }}
        
        .tree-folder:hover {{
            text-decoration: underline;
        }}
        
        .tree-children {{
            display: none;
            margin-left: 20px;
        }}
        
        .tree-file {{
            margin: 5px 0;
            color: var(--text-color);
        }}
        
        .file-size {{
            color: #999;
            font-size: 0.8rem;
            margin-left: 10px;
        }}
        
        .file-type-python {{
            color: #3572A5;
        }}
        
        .file-type-javascript {{
            color: #f1e05a;
        }}
        
        .file-type-web {{
            color: #e34c26;
        }}
        
        .file-type-config {{
            color: #6e6e6e;
        }}
        
        .file-type-documentation {{
            color: #083fa1;
        }}
        
        .changes-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .changes-section {{
            background-color: var(--card-background);
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }}
        
        .changes-list {{
            list-style-type: none;
            padding: 0;
            margin: 0;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .changes-list li {{
            padding: 5px 0;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .changes-list.added li {{
            color: var(--secondary-color);
        }}
        
        .changes-list.modified li {{
            color: #FBBC05;
        }}
        
        .changes-list.deleted li {{
            color: var(--accent-color);
        }}
        
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .service-card {{
            background-color: var(--card-background);
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 15px;
            border-top: 4px solid var(--primary-color);
        }}
        
        .service-microservice {{
            border-top-color: var(--primary-color);
        }}
        
        .service-backend {{
            border-top-color: var(--secondary-color);
        }}
        
        .service-frontend {{
            border-top-color: var(--accent-color);
        }}
        
        .service-header {{
            font-weight: bold;
            font-size: 1.2rem;
            margin-bottom: 10px;
        }}
        
        .service-type {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8rem;
            margin-bottom: 10px;
            background-color: #f0f0f0;
        }}
        
        .service-path {{
            font-size: 0.9rem;
            color: #666;
        }}
        
        .tabs {{
            display: flex;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .tab {{
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
        }}
        
        .tab.active {{
            border-bottom-color: var(--primary-color);
            font-weight: bold;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
            border-top: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>
    <header>
        <h1>{project_name} Workspace Visualization</h1>
        <p>Generated on {indexed_at}</p>
    </header>
    
    <div class="container">
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-value">{file_count}</div>
                <div class="summary-label">Files</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{directory_count}</div>
                <div class="summary-label">Directories</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{total_size_mb:.2f} MB</div>
                <div class="summary-label">Total Size</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{len(self.index.get("file_types", {}))}</div>
                <div class="summary-label">File Types</div>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab active" data-tab="overview">Overview</div>
            <div class="tab" data-tab="structure">Directory Structure</div>
            <div class="tab" data-tab="changes">Changes</div>
            <div class="tab" data-tab="services">Services</div>
        </div>
        
        <div class="tab-content active" id="overview">
            <div class="card">
                <h2>File Type Distribution</h2>
                {file_type_chart}
            </div>
            
            <div class="card">
                <h2>File Extensions</h2>
                {file_extension_chart}
            </div>
        </div>
        
        <div class="tab-content" id="structure">
            <div class="card">
                <h2>Directory Structure</h2>
                <div class="directory-tree">
                    {directory_tree}
                </div>
            </div>
        </div>
        
        <div class="tab-content" id="changes">
            <div class="card">
                <h2>Recent Changes</h2>
                {changes_section}
            </div>
        </div>
        
        <div class="tab-content" id="services">
            <div class="card">
                <h2>Project Services</h2>
                {services_section}
            </div>
        </div>
    </div>
    
    <footer>
        <p>grimOS Workspace Visualizer &copy; {project_name} Team</p>
    </footer>
    
    <script>
        // Toggle folder expansion
        function toggleFolder(element) {{
            const children = element.parentElement.querySelector('.tree-children');
            if (children.style.display === 'block') {{
                children.style.display = 'none';
            }} else {{
                children.style.display = 'block';
            }}
        }}
        
        // Tab switching
        document.addEventListener('DOMContentLoaded', function() {{
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => {{
                tab.addEventListener('click', () => {{
                    // Remove active class from all tabs
                    tabs.forEach(t => t.classList.remove('active'));
                    
                    // Add active class to clicked tab
                    tab.classList.add('active');
                    
                    // Hide all tab content
                    document.querySelectorAll('.tab-content').forEach(content => {{
                        content.classList.remove('active');
                    }});
                    
                    // Show selected tab content
                    const tabId = tab.getAttribute('data-tab');
                    document.getElementById(tabId).classList.add('active');
                }});
            }});
            
            // Expand first level of directories
            document.querySelectorAll('.tree-item').forEach(item => {{
                if (!item.parentElement.classList.contains('tree-children')) {{
                    const folder = item.querySelector('.tree-folder');
                    if (folder) {{
                        toggleFolder(folder);
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
"""
        
        # Write HTML to file
        with open(output_path, 'w') as f:
            f.write(html)
            
        print(f"Workspace visualization created at {output_path}")


def main():
    """Main entry point for the workspace visualizer."""
    parser = argparse.ArgumentParser(description='grimOS Workspace Visualizer')
    parser.add_argument('--index', default='workspace_index.json', help='Path to workspace index file')
    parser.add_argument('--config', default='scripts/workspace_config.json', help='Path to configuration file')
    parser.add_argument('--output', default='workspace_visualization.html', help='Output HTML file path')
    
    args = parser.parse_args()
    
    try:
        visualizer = WorkspaceVisualizer(args.index, args.config)
        visualizer.generate_html(args.output)
        return 0
    except Exception as e:
        print(f"Error generating visualization: {e}")
        return 1


if __name__ == "__main__":
    exit(main())