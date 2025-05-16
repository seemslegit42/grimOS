.PHONY: up down build logs dev test migrate migrate-auto help

# Default target executed when no arguments are given to make.
default: help

# Start all services
up:
	docker-compose up -d

# Start all services and follow logs
up-logs:
	docker-compose up

# Stop all services
down:
	docker-compose down

# Rebuild all services
build:
	docker-compose build

# View logs
logs:
	docker-compose logs -f

# Start all services in development mode
dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run the test suite
test:
	cd auth && python -m pytest
	cd api-gateway && npm test

# Generate a new migration
migrate-auto:
	docker-compose exec auth alembic revision --autogenerate -m "$(MESSAGE)"

# Apply migrations
migrate:
	docker-compose exec auth alembic upgrade head

# Create initial admin user
create-admin:
	docker-compose exec auth python -c "from app.db.session import SessionLocal; from app.db.init_db import init_db; init_db(SessionLocal())"

# View help information
help:
	@echo "grimOS Microservices"
	@echo ""
	@echo "Usage:"
	@echo "  make up          Start all services in detached mode"
	@echo "  make up-logs     Start all services and follow logs"
	@echo "  make down        Stop all services"
	@echo "  make build       Rebuild all services"
	@echo "  make logs        View logs of all services"
	@echo "  make dev         Start all services in development mode"
	@echo "  make test        Run all tests"
	@echo "  make migrate     Apply database migrations"
	@echo "  make migrate-auto MESSAGE=\"Your message\" Generate a new migration"
	@echo "  make create-admin Create the initial admin user"
	@echo "  make help        Show this help message"
