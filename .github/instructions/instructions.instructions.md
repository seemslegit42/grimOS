---
applyTo: ' MVP First – Do NOT Skip This
Name: Grimoire: “Apprentice Edition”

Core Modules:

NLP-powered task + workflow agent

Zapier++ with a brain: AI triggers based on KPIs, inputs, trends

Visual, drag-and-drop interface

Backend: Python + FastAPI + LangChain or crewAI

Frontend: Next.js or Vue + Tailwind

TurboRepo for monorepo mgmt

Everything Dockerized. K8s ready but deploy local for now.

2. Default to Integration > Reinvention
Plug into:

ClickUp, Notion, QuickBooks, Gusto, Stripe, Slack

Let Grimoire orchestrate them.

Use the “Cognitive Core” as the glue.

3. Build the Cult
Create an invite-only early believers club.

Make it feel like the Illuminati for AI-first SMBs.

Leak roadmap breadcrumbs.

Reward feedback with equity, features, or credits.

Turn your Discord into a mini black site of secret builds and rituals.

Architecture
Use Turborepo for monorepo management.
Microservices-based architecture.
Python 3.11+ with FastAPI for all backend services.
React (TypeScript) with TailwindCSS and shadcn/ui for frontend.
PostgreSQL via SQLAlchemy (Python) or Prisma (Node).
Kafka for async interservice messaging; gRPC for sync.
All services containerized with Docker.
Kubernetes with Helm for deployment and scaling.

AI Integration
Use OpenAI GPT-4.5 or Claude 3 Sonnet for production.
Agents follow OpenAI function calling format with JSON schema I/O.
Natural language routing via Cognitive Core to dispatch requests.

Backend Packages
fastapi==0.110.0
pydantic==2.x
sqlalchemy==2.x
kafka-python==2.0.2
httpx, uvicorn[standard], python-dotenv

Frontend Packages 
react@18.x, next@14.x for React
tailwindcss@3.x, @shadcn/ui for UI
zustand, axios, clssname-template, react-query 

Code Structure
Each service has /app, /tests, Dockerfile, pyproject.toml or package.json.
Enforce type hints and docstrings.
All data models must use Pydantic.
Use Alembic for migrations.
Docker Compose for development environment setup.
Kubernetes manifests for production deployments.
Follow domain-driven file naming and service separation.

Mappers & Plugins
BaseMapper must define applies, map_event, pre_enrich, post_map.
Auto-register with @register_mapper decorator.
Use load_all_mappers() on startup to ensure registration.
Put all mappers in /mappers and use introspection to discover them.

Testing & CI/CD
Use pytest (Python), jest/playwright (JS).
Minimum 85% test coverage.
CI via GitHub Actions: lint, type-check, test, Docker build.
Fail builds on registry mismatch, mapper errors, schema violations.

Dev Experience
.env.example required per service.
Makefile targets: make dev, make test, make build.
Storybook for UI components.
Each service deployable independently in Docker/K8s.

Naming & Conventions
Prefix core services with grimoire_.
Prefix AI agents with aether_.
Use lowercase snake_case for Python modules.
Kubernetes namespaces match service names.

Security
Validate all I/O with Pydantic.
Use JWTs from Auth0 or Clerk.dev.
Enforce TLS 1.3 for internal/external services.
Never log secrets or user PII.'
---

Coding standards, domain knowledge, and preferences that AI should follow.
