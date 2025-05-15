# grimOS Remote Workspace Index

This tool provides a comprehensive solution for indexing, analyzing, and visualizing the grimOS workspace structure, enabling efficient remote development and collaboration.

## Features

* **Workspace Indexing**: Tracks files, directories, and metadata across the entire project
* **Service Analysis**: Identifies microservices, their dependencies, and communication patterns
* **Visualization**: Generates interactive HTML visualizations of the workspace structure
* **Remote Sync**: Synchronizes the workspace to remote locations for distributed development
* **Change Tracking**: Detects added, modified, and deleted files between indexing runs

## Installation

No additional installation is required. The Remote Workspace Index tools are built using Python and are included in the grimOS repository.

## Usage

### Using the Makefile

The simplest way to use the Remote Workspace Index is through the provided Makefile:

```bash
# Navigate to the scripts directory
cd scripts

# Build the workspace index, analyze services, and generate visualization
make

# Build only the workspace index
make index

# Analyze services (requires index)
make analyze

# Generate visualization (requires index)
make visualize

# Sync to remote (requires configuration)
make sync

# Run all tasks
make run-all

# Clean generated files
make clean

# Show help
make help
```

### Using the Python Scripts Directly

You can also run the Python scripts directly:

```bash
# Build workspace index
python scripts/workspace_indexer.py --config scripts/workspace_config.json

# Analyze services
python scripts/service_analyzer.py --index workspace_index.json --output service_analysis.json

# Generate visualization
python scripts/workspace_visualizer.py --index workspace_index.json --config scripts/workspace_config.json --output workspace_visualization.html

# Run all tasks
python scripts/remote_workspace_manager.py --all
```

## Configuration

The Remote Workspace Index is configured through the `scripts/workspace_config.json` file. Here are the key configuration options:

```json
{
  "projectName": "grimOS",
  "indexFile": "workspace_index.json",
  "indexConfigs": {
    "excludeDirs": [".git", "node_modules", "__pycache__", ".turbo", "build", "dist", ".next"],
    "excludeExtensions": [".pyc", ".pyo", ".o", ".obj", ".exe", ".bin", ".log", ".lock"],
    "includeContent": false,
    "trackChanges": true,
    "maxFileSize": 1048576
  },
  "remoteSync": {
    "enabled": false,
    "remotePath": "",
    "syncInterval": 3600,
    "syncCommand": "",
    "excludeFromSync": [".git", "node_modules", "__pycache__"]
  },
  "visualization": {
    "enabled": true,
    "generateGraph": true,
    "graphOutputPath": "workspace_graph.html"
  }
}
```

### Remote Sync Configuration

To enable remote syncing, update the `remoteSync` section in the configuration:

```json
"remoteSync": {
  "enabled": true,
  "remotePath": "user@remote-server:/path/to/grimOS",
  "syncInterval": 3600,
  "syncCommand": "rsync -avz --delete --exclude-from=.rsyncignore . user@remote-server:/path/to/grimOS/",
  "excludeFromSync": [
    ".git",
    "node_modules",
    "__pycache__"
  ]
}
```

## Output Files

The Remote Workspace Index generates the following files:

* `workspace_index.json`: Contains the complete workspace index
* `service_analysis.json`: Contains the service analysis results
* `workspace_visualization.html`: Interactive visualization of the workspace

## Visualization

The generated visualization provides:

* Directory structure tree
* File type distribution charts
* File extension statistics
* Recent changes tracking
* Service relationship diagrams

To view the visualization, open `workspace_visualization.html` in a web browser.

## Integration with Development Workflow

### Continuous Integration

Add the workspace indexing to your CI pipeline:

```yaml
# In your CI configuration
steps:
  - name: Build Workspace Index
    run: |
      cd scripts
      make index analyze
```

### Pre-commit Hook

Create a pre-commit hook to update the workspace index:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Update workspace index
python scripts/workspace_indexer.py --config scripts/workspace_config.json
```

### Scheduled Updates

Set up a cron job to periodically update the workspace index and sync to remote:

```bash
# Update workspace index and sync every hour
0 * * * * cd /path/to/grimOS && python scripts/remote_workspace_manager.py --all
```

## Troubleshooting

### Common Issues

* **Index build fails**: Ensure you have the necessary permissions to read all files in the workspace
* **Visualization not showing**: Check that the workspace index was built successfully
* **Remote sync fails**: Verify SSH keys are set up correctly for the remote server

### Logs

Check the following logs for troubleshooting:

* Console output from the scripts
* `sync.log`: Created when syncing to remote

## Contributing

Contributions to the Remote Workspace Index are welcome! Please follow the grimOS contribution guidelines.

## License

The Remote Workspace Index is part of the grimOS project and is licensed under the same terms as the main project.
