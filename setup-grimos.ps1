# grimOS Setup Script
# This script sets up the grimOS development environment

Write-Host "Setting up grimOS development environment..." -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pnpm install

# Set up backend services
Write-Host "Setting up backend services..." -ForegroundColor Yellow
cd apps/backend
pip install -r requirements.txt
cd ../..

# Set up AI services
Write-Host "Setting up AI services..." -ForegroundColor Yellow
cd services/ai
pip install -r requirements.txt
cd ../..

# Start Docker services
Write-Host "Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "grimOS development environment setup complete!" -ForegroundColor Green
Write-Host "Run 'pnpm dev' to start the development servers" -ForegroundColor Green
