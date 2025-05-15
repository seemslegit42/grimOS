### Setup script for grimOS development environment

# Create necessary directories
function Ensure-Directory {
    param (
        [string]$Path
    )
    
    if (-not (Test-Path $Path)) {
        Write-Host "Creating directory: $Path" -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

Write-Host "Setting up grimOS development environment..." -ForegroundColor Green

# Ensure service directories exist
$services = @(
    "services/composable-runes/app/api/api_v1/endpoints",
    "services/composable-runes/app/core",
    "services/composable-runes/app/models",
    "services/composable-runes/app/schemas",
    "services/composable-runes/app/services",
    "services/interoperability/app/api/api_v1/endpoints",
    "services/interoperability/app/core",
    "services/interoperability/app/models",
    "services/interoperability/app/schemas",
    "services/interoperability/app/services"
)

foreach ($service in $services) {
    Ensure-Directory -Path $service
}

# Start Docker services for development
Write-Host "Starting Docker containers for development..." -ForegroundColor Yellow
docker-compose -f docker-compose.dev.yml up -d

Write-Host "grimOS development environment is ready!" -ForegroundColor Green
Write-Host "You can access the following services:" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  - API Gateway: http://localhost:8080" -ForegroundColor Cyan
Write-Host "  - Cognitive Core API: http://localhost:8001" -ForegroundColor Cyan
Write-Host "  - Composable Runes API: http://localhost:8002" -ForegroundColor Cyan
Write-Host "  - Interoperability API: http://localhost:8003" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "To run the frontend in development mode with hot reloading:" -ForegroundColor Cyan
Write-Host "  cd apps/frontend" -ForegroundColor Cyan
Write-Host "  pnpm dev" -ForegroundColor Cyan
