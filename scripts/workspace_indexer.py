#!/usr/bin/env python3
"""
Workspace Indexer for grimOS

This script builds a comprehensive index of the grimOS workspace,
tracking files, directories, and metadata to facilitate remote development.

Usage:
    python workspace_indexer.py [--config CONFIG_FILE] [--output OUTPUT_FILE] [--sync]

Author: grimOS Team
"""

import os
import json
import time
import argparse
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple


class WorkspaceIndexer:
    """
    Builds and maintains an index of the grimOS workspace.
    
    This class handles the creation of a detailed workspace index,
    including file metadata, directory structure, and optional content indexing.
    It supports remote synchronization and incremental updates.
    """
    
    def __init__(self, config_path: str = "scripts/workspace_config.json"):
        """
        Initialize the workspace indexer with configuration.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.root_dir = os.getcwd()
        self.index_file = self.config.get("indexFile", "workspace_index.json")
        self.previous_index = self._load_previous_index()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load the workspace configuration from a JSON file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dict containing configuration settings
        """
        default_config = {
            "projectName": "grimOS",
            "indexFile": "workspace_index.json",
            "indexConfigs": {
                "excludeDirs": [
                    ".git", "node_modules", "__pycache__", 
                    ".turbo", "build", "dist", ".next"
                ],
                "excludeExtensions": [
                    ".pyc", ".pyo", ".o", ".obj", ".exe", ".bin", 
                    ".log", ".lock", ".swp", ".swo"
                ],
                "includeContent": False,
                "trackChanges": True,
                "maxFileSize": 1048576  # 1MB
            },
            "remoteSync": {
                "enabled": False,
                "remotePath": "",
                "syncInterval": 3600,
                "syncCommand": "",
                "excludeFromSync": []
            }
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # Merge user config with default config
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in default_config and isinstance(default_config[key], dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
            except Exception as e:
                print(f"Error loading config from {config_path}: {e}")
                print("Using default configuration")
        else:
            print(f"Config file {config_path} not found. Using default configuration.")
            # Create default config file
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
                
        return default_config
    
    def _load_previous_index(self) -> Dict[str, Any]:
        """
        Load the previous workspace index if it exists.
        
        Returns:
            Dict containing the previous index or an empty dict
        """
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading previous index: {e}")
        return {}
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate a hash for the file content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SHA-256 hash of the file content
        """
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.config["indexConfigs"]["maxFileSize"]:
                # For large files, just hash the first and last 4KB
                with open(file_path, 'rb') as f:
                    content = f.read(4096)
                    f.seek(-4096, 2)
                    content += f.read(4096)
            else:
                with open(file_path, 'rb') as f:
                    content = f.read()
            
            return hashlib.sha256(content).hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return "error-calculating-hash"
    
    def _is_excluded(self, path: str, is_dir: bool = False) -> bool:
        """
        Check if a path should be excluded from indexing.
        
        Args:
            path: Path to check
            is_dir: Whether the path is a directory
            
        Returns:
            True if the path should be excluded, False otherwise
        """
        rel_path = os.path.relpath(path, self.root_dir)
        
        # Check if in excluded directories
        if is_dir:
            basename = os.path.basename(path)
            if basename in self.config["indexConfigs"]["excludeDirs"]:
                return True
                
        # Check path patterns
        for excluded_dir in self.config["indexConfigs"]["excludeDirs"]:
            if rel_path.startswith(excluded_dir + os.sep) or rel_path == excluded_dir:
                return True
        
        # Check file extensions
        if not is_dir:
            _, ext = os.path.splitext(path)
            if ext.lower() in self.config["indexConfigs"]["excludeExtensions"]:
                return True
                
        return False
    
    def _get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Get metadata for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dict containing file metadata
        """
        rel_path = os.path.relpath(file_path, self.root_dir)
        
        try:
            stat_info = os.stat(file_path)
            file_size = stat_info.st_size
            modified_time = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            
            # Get file type
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            # Determine file type category
            file_type = "unknown"
            if ext in ['.py', '.pyi']:
                file_type = "python"
            elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                file_type = "javascript"
            elif ext in ['.html', '.htm', '.css', '.scss', '.sass', '.less']:
                file_type = "web"
            elif ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                file_type = "config"
            elif ext in ['.md', '.txt', '.rst']:
                file_type = "documentation"
            elif ext in ['.sql']:
                file_type = "database"
            elif ext in ['.proto']:
                file_type = "proto"
            elif ext in ['.sh', '.bash', '.zsh', '.bat', '.cmd', '.ps1']:
                file_type = "script"
            
            metadata = {
                "path": rel_path,
                "size": file_size,
                "modified": modified_time,
                "type": file_type,
                "extension": ext
            }
            
            # Calculate hash if tracking changes
            if self.config["indexConfigs"]["trackChanges"]:
                metadata["hash"] = self._calculate_file_hash(file_path)
                
            # Include content if configured
            if self.config["indexConfigs"]["includeContent"] and file_size <= self.config["indexConfigs"]["maxFileSize"]:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        metadata["content"] = f.read()
                except UnicodeDecodeError:
                    metadata["content"] = "Binary or non-UTF-8 content"
                    
            return metadata
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return {
                "path": rel_path,
                "error": str(e),
                "type": "error"
            }
    
    def build_index(self) -> Dict[str, Any]:
        """
        Build the workspace index.
        
        Returns:
            Dict containing the workspace index
        """
        start_time = time.time()
        
        index = {
            "project": self.config["projectName"],
            "indexed_at": datetime.now().isoformat(),
            "root_directory": self.root_dir,
            "files": [],
            "directories": [],
            "file_count": 0,
            "directory_count": 0,
            "file_types": {},
            "file_extensions": {},
            "total_size": 0,
            "build_time": 0
        }
        
        # Track changes if previous index exists
        changes = {
            "added": [],
            "modified": [],
            "deleted": []
        }
        
        previous_files = {}
        if self.previous_index and "files" in self.previous_index:
            previous_files = {file_info["path"]: file_info for file_info in self.previous_index["files"]}
        
        # Walk the directory tree
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Filter out excluded directories
            dirnames[:] = [d for d in dirnames if not self._is_excluded(os.path.join(dirpath, d), True)]
            
            # Process directory
            rel_path = os.path.relpath(dirpath, self.root_dir)
            if rel_path != '.':
                index["directories"].append(rel_path)
                index["directory_count"] += 1
            
            # Process files
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                
                # Skip excluded files
                if self._is_excluded(file_path):
                    continue
                
                # Get file metadata
                file_info = self._get_file_metadata(file_path)
                rel_path = file_info["path"]
                
                # Track file type statistics
                file_type = file_info.get("type", "unknown")
                if file_type in index["file_types"]:
                    index["file_types"][file_type] += 1
                else:
                    index["file_types"][file_type] = 1
                
                # Track file extension statistics
                ext = file_info.get("extension", "")
                if ext:
                    if ext in index["file_extensions"]:
                        index["file_extensions"][ext] += 1
                    else:
                        index["file_extensions"][ext] = 1
                
                # Track changes
                if self.config["indexConfigs"]["trackChanges"]:
                    if rel_path in previous_files:
                        prev_file = previous_files[rel_path]
                        if "hash" in file_info and "hash" in prev_file and file_info["hash"] != prev_file["hash"]:
                            changes["modified"].append(rel_path)
                    else:
                        changes["added"].append(rel_path)
                
                # Add file to index
                index["files"].append(file_info)
                index["file_count"] += 1
                index["total_size"] += file_info.get("size", 0)
        
        # Find deleted files
        if self.config["indexConfigs"]["trackChanges"]:
            current_files = {file_info["path"] for file_info in index["files"]}
            for path in previous_files:
                if path not in current_files:
                    changes["deleted"].append(path)
            
            # Add changes to index
            index["changes"] = changes
            index["changes_count"] = {
                "added": len(changes["added"]),
                "modified": len(changes["modified"]),
                "deleted": len(changes["deleted"])
            }
        
        # Calculate build time
        index["build_time"] = time.time() - start_time
        
        # Save the index
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"Workspace index created at {self.index_file}")
        print(f"Indexed {index['file_count']} files in {index['directory_count']} directories")
        print(f"Total size: {index['total_size'] / (1024*1024):.2f} MB")
        print(f"Build time: {index['build_time']:.2f} seconds")
        
        if self.config["indexConfigs"]["trackChanges"] and self.previous_index:
            print(f"Changes: {len(changes['added'])} added, {len(changes['modified'])} modified, {len(changes['deleted'])} deleted")
        
        return index
    
    def sync_to_remote(self) -> bool:
        """
        Sync the workspace to a remote location.
        
        Returns:
            True if sync was successful, False otherwise
        """
        if not self.config["remoteSync"]["enabled"]:
            print("Remote sync not enabled in configuration")
            return False
            
        if not self.config["remoteSync"]["remotePath"]:
            print("Remote path not configured")
            return False
        
        try:
            # Use custom sync command if provided
            if self.config["remoteSync"]["syncCommand"]:
                command = self.config["remoteSync"]["syncCommand"]
            else:
                # Default to rsync for Linux/WSL
                exclude_args = ' '.join([f'--exclude="{item}"' for item in self.config["remoteSync"]["excludeFromSync"]])
                command = f'rsync -avz --delete {exclude_args} {self.root_dir}/ {self.config["remoteSync"]["remotePath"]}/'
            
            print(f"Syncing to remote: {self.config['remoteSync']['remotePath']}")
            print(f"Running command: {command}")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Log sync results
            log_file = os.path.join(self.root_dir, "sync.log")
            with open(log_file, 'w') as f:
                f.write(f"Sync at: {datetime.now().isoformat()}\n")
                f.write(f"Command: {command}\n")
                f.write(f"Exit code: {result.returncode}\n")
                f.write(f"Output:\n{result.stdout}\n")
                if result.stderr:
                    f.write(f"Errors:\n{result.stderr}\n")
            
            if result.returncode == 0:
                print("Remote sync completed successfully")
                return True
            else:
                print(f"Remote sync failed with exit code {result.returncode}")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error syncing to remote: {e}")
            return False


def main():
    """Main entry point for the workspace indexer."""
    parser = argparse.ArgumentParser(description='grimOS Workspace Indexer')
    parser.add_argument('--config', default='scripts/workspace_config.json', help='Configuration file path')
    parser.add_argument('--output', help='Output file path for the index')
    parser.add_argument('--sync', action='store_true', help='Sync to remote after indexing')
    
    args = parser.parse_args()
    
    # Initialize indexer
    indexer = WorkspaceIndexer(args.config)
    
    # Override output file if specified
    if args.output:
        indexer.index_file = args.output
    
    # Build index
    index = indexer.build_index()
    
    # Sync to remote if requested
    if args.sync:
        indexer.sync_to_remote()
    
    return 0


if __name__ == "__main__":
    exit(main())