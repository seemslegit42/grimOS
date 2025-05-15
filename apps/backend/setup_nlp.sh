#!/bin/bash
# Setup script for spaCy NLP components

# Exit on error
set -e

echo "=== Setting up spaCy for GrimOS ScrollWeaver ==="

# Ensure virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d ".venv" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    else
        echo "Error: Virtual environment not found. Please create and activate it first."
        exit 1
    fi
fi

# Install spaCy
echo "Installing spaCy..."
pip install spacy

# Download English model (medium-sized model with good balance of accuracy and performance)
echo "Downloading spaCy English language model..."
python -m spacy download en_core_web_sm

# Create NLP directories if they don't exist
echo "Creating NLP data directories..."
mkdir -p app/services/nlp/models
mkdir -p app/services/nlp/data

echo "=== spaCy setup complete! ==="
echo "You can now use the ScrollWeaver natural language processing capabilities."
