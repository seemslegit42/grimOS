# GrimOS Monorepo

GrimOS is a next-generation operating system built with a microservices architecture using Turborepo.

## Project Structure

```
grimOS/
├── apps/
│   ├── frontend/         # Next.js frontend
│   └── backend/          # FastAPI backend
├── packages/
│   └── shared/           # Shared code (types, utils)
├── turbo.json            # Turborepo configuration
└── package.json          # Root package.json
```

## Getting Started

### Prerequisites

* Node.js 20+
* Python 3.11+
* pnpm 9+
* Docker and Docker Compose (optional, for local development)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/grimOS.git
cd grimOS
```

2. Install dependencies:

```bash
pnpm install
```

3. Set up environment variables:

```bash
cp apps/frontend/.env.example apps/frontend/.env.local
cp apps/backend/.env.example apps/backend/.env
```

### Development

Start all applications in development mode:

```bash
pnpm dev
```

Or start individual applications:

```bash
# Frontend only
pnpm --filter @grimos/frontend dev

# Backend only
pnpm --filter @grimos/backend dev
```

### Building

Build all applications:

```bash
pnpm build
```

### Testing

Run tests for all applications:

```bash
pnpm test
```

### Using Docker

Start the entire stack with Docker Compose:

```bash
docker-compose up -d
```

## Migration Guide

This project was migrated from a monolithic structure to a Turborepo monorepo. The migration process involved:

1. Setting up a Turborepo structure with apps and packages directories
2. Moving the Next.js frontend to apps/frontend
3. Moving the FastAPI backend to apps/backend
4. Creating a shared package for common code
5. Configuring build pipelines and caching

## License

[MIT](LICENSE)
