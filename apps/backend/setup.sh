#!/bin/bash
# Setup script for GrimOS Backend

# Exit on error
set -e

echo "=== Setting up GrimOS Backend ==="

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
fi

# Initialize the database
echo "Initializing database..."
# Check if postgres is running (assuming local development)
pg_isready -h localhost -p 5432 -U postgres -d postgres -t 5 || {
    echo "PostgreSQL is not running. Please start PostgreSQL and try again."
    exit 1
}

# Check if database exists, create if it doesn't
psql -h localhost -p 5432 -U postgres -c "SELECT 1 FROM pg_database WHERE datname = 'grimos'" | grep -q 1 || {
    echo "Creating grimos database..."
    psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE grimos"
}

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Set up NLP components (optional)
read -p "Do you want to set up NLP components for ScrollWeaver? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting up NLP components..."
    chmod +x setup_nlp.sh
    ./setup_nlp.sh
fi

echo "=== Setup complete! ==="
echo "You can now start the server with: uvicorn app.main:app --reload --port 8000"
