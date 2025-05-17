.PHONY: up down restart logs psql redis-cli monitoring kong all clean help

# Default environment
ENV ?= dev

# Docker compose files
DC_FILE = docker-compose.yml
DC_MONITORING = docker-compose.monitoring.yml
DC_KONG = docker-compose.kong.yml
DC_FULL = docker-compose.full.yml

# Start commands
up:
	docker-compose up -d

monitoring:
	docker-compose -f $(DC_MONITORING) up -d

kong:
	docker-compose -f $(DC_KONG) up -d

all:
	docker-compose -f $(DC_FULL) up -d

# Stop commands
down:
	docker-compose down

down-monitoring:
	docker-compose -f $(DC_MONITORING) down

down-kong:
	docker-compose -f $(DC_KONG) down

down-all:
	docker-compose -f $(DC_FULL) down

# Restart commands
restart:
	docker-compose restart

restart-monitoring:
	docker-compose -f $(DC_MONITORING) restart

restart-kong:
	docker-compose -f $(DC_KONG) restart

restart-all:
	docker-compose -f $(DC_FULL) restart

# Logs
logs:
	docker-compose logs -f

# Database access
psql:
	docker-compose exec db psql -U postgres -d grimos

# Redis CLI
redis-cli:
	docker-compose exec redis redis-cli

# Clean everything
clean:
	docker-compose down -v
	docker-compose -f $(DC_MONITORING) down -v
	docker-compose -f $(DC_KONG) down -v

# Migration commands
migrations-create:
	docker-compose exec backend alembic revision --autogenerate -m "$(name)"

migrations-apply:
	docker-compose exec backend alembic upgrade head

# Help
help:
	@echo "GrimOS Backend Management Commands"
	@echo "--------------------------------"
	@echo "up                - Start the basic stack (DB, Redis, API)"
	@echo "monitoring        - Start monitoring stack (Prometheus, Grafana)"
	@echo "kong              - Start API Gateway stack (Kong, Konga)"
	@echo "all               - Start all services"
	@echo "down              - Stop the basic stack"
	@echo "down-monitoring   - Stop monitoring stack"
	@echo "down-kong         - Stop API Gateway stack"
	@echo "down-all          - Stop all services"
	@echo "restart           - Restart the basic stack"
	@echo "restart-monitoring- Restart monitoring stack"
	@echo "restart-kong      - Restart API Gateway stack"
	@echo "restart-all       - Restart all services"
	@echo "logs              - Show logs from all services"
	@echo "psql              - Connect to PostgreSQL CLI"
	@echo "redis-cli         - Connect to Redis CLI"
	@echo "clean             - Remove all containers and volumes"
	@echo "migrations-create - Create new migration (use name=migration_name)"
	@echo "migrations-apply  - Apply all pending migrations"
