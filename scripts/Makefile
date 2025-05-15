# grimOS Remote Workspace Manager Makefile

.PHONY: all index analyze visualize sync clean help

PYTHON := python3
SCRIPTS_DIR := scripts
CONFIG_FILE := $(SCRIPTS_DIR)/workspace_config.json
INDEX_FILE := workspace_index.json
SERVICE_ANALYSIS_FILE := service_analysis.json
VISUALIZATION_FILE := workspace_visualization.html

# Default target
all: index analyze visualize

# Build workspace index
index:
	@echo "Building workspace index..."
	@$(PYTHON) $(SCRIPTS_DIR)/workspace_indexer.py --config $(CONFIG_FILE)

# Analyze services
analyze: index
	@echo "Analyzing services..."
	@$(PYTHON) $(SCRIPTS_DIR)/service_analyzer.py --index $(INDEX_FILE) --output $(SERVICE_ANALYSIS_FILE)

# Generate visualization
visualize: index
	@echo "Generating visualization..."
	@$(PYTHON) $(SCRIPTS_DIR)/workspace_visualizer.py --index $(INDEX_FILE) --config $(CONFIG_FILE) --output $(VISUALIZATION_FILE)

# Sync to remote
sync: index
	@echo "Syncing to remote..."
	@$(PYTHON) $(SCRIPTS_DIR)/workspace_indexer.py --config $(CONFIG_FILE) --sync

# Run all tasks
run-all:
	@echo "Running all workspace management tasks..."
	@$(PYTHON) $(SCRIPTS_DIR)/remote_workspace_manager.py --all

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f $(INDEX_FILE) $(SERVICE_ANALYSIS_FILE) $(VISUALIZATION_FILE)

# Help
help:
	@echo "grimOS Remote Workspace Manager"
	@echo ""
	@echo "Usage:"
	@echo "  make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all         Build index, analyze services, and generate visualization (default)"
	@echo "  index       Build workspace index"
	@echo "  analyze     Analyze services (requires index)"
	@echo "  visualize   Generate visualization (requires index)"
	@echo "  sync        Sync to remote (requires index)"
	@echo "  run-all     Run all tasks using the remote workspace manager"
	@echo "  clean       Remove generated files"
	@echo "  help        Show this help message"