# GrimOS Migration Guide: Monolithic to Turborepo Monorepo

This guide outlines the steps to migrate the GrimOS project from a monolithic structure to a Turborepo monorepo architecture.

## Step 1: Setup Turborepo Configuration

1. Update the root `package.json` to include workspaces and monorepo scripts:

```json
{
  "name": "grimos",
  "version": "0.0.0",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "format": "prettier --write \"**/*.{ts,tsx,md}\"",
    "test": "turbo test",
    "clean": "turbo clean && rm -rf node_modules"
  }
}
```

2. Update `turbo.json` to configure the build pipeline:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "globalEnv": ["NODE_ENV", "PORT", "NEXT_PUBLIC_API_URL"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true,
      "dependsOn": ["^build"]
    },
    "start": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "test/**/*.ts", "test/**/*.tsx"]
    },
    "clean": {
      "cache": false
    }
  }
}
```

## Step 2: Create Shared Package

1. Create a shared package for common code:

```
packages/shared/
├── package.json
├── tsconfig.json
├── tsup.config.ts
└── src/
    ├── index.ts
    ├── types/
    │   └── index.ts
    └── utils/
        └── index.ts
```

2. Configure the shared package's `package.json`:

```json
{
  "name": "@grimos/shared",
  "version": "0.0.0",
  "private": true,
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "files": ["dist/**"],
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch",
    "lint": "eslint src/",
    "clean": "rm -rf dist"
  }
}
```

## Step 3: Setup Frontend App

1. Create the frontend app structure:

```
apps/frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
├── lib/
├── public/
├── styles/
├── package.json
├── next.config.js
├── tsconfig.json
├── postcss.config.js
└── tailwind.config.js
```

2. Configure the frontend app's `package.json`:

```json
{
  "name": "@grimos/frontend",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@grimos/shared": "*",
    "next": "15.3.1",
    "react": "^19.1.0",
    "react-dom": "^19.1.0"
  }
}
```

3. Configure Next.js to work with the monorepo:

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@grimos/shared'],
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL + '/:path*',
      },
    ]
  },
}

module.exports = nextConfig
```

## Step 4: Setup Backend App

1. Create the backend app structure:

```
apps/backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── core/
│   └── models/
├── tests/
├── package.json
├── pyproject.toml
├── Dockerfile
└── .env.example
```

2. Configure the backend app's `package.json`:

```json
{
  "name": "@grimos/backend",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000",
    "start": "cd app && uvicorn main:app --host 0.0.0.0 --port 8000",
    "build": "echo 'No build step for Python backend'",
    "lint": "cd app && ruff check .",
    "format": "cd app && ruff format .",
    "test": "cd app && pytest"
  }
}
```

3. Configure the Python backend with `pyproject.toml`:

```toml
[project]
name = "grimos-backend"
version = "0.1.0"
description = "GrimOS Backend API"
requires-python = ">=3.11,<4.0"
dependencies = [
    "fastapi==0.110.0",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
    "uvicorn[standard]>=0.25.0",
    "python-dotenv>=1.0.0"
]
```

## Step 5: Move Existing Code

1. Move Next.js frontend code:

   * Copy `app/layout.tsx` and `app/page.tsx` to `apps/frontend/app/`
   * Copy `styles/` to `apps/frontend/styles/`
   * Copy `components/` to `apps/frontend/components/`
   * Copy configuration files like `next.config.ts`, `tsconfig.json`, etc.

2. Move FastAPI backend code:
   * Copy `app/fastapi-backend/backend/` to `apps/backend/`
   * Copy `app/fastapi-backend/backend/app/` to `apps/backend/app/`

## Step 6: Configure Docker and Local Development

1. Create a `docker-compose.yml` file for local development:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: grimos
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./apps/backend:/app
    environment:
      - DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/grimos
      - ALLOWED_ORIGINS=http://localhost:3000
    depends_on:
      - postgres

volumes:
  postgres_data:
```

## Step 7: Install Dependencies and Test

1. Install dependencies:

```bash
pnpm install
```

2. Build the shared package:

```bash
pnpm --filter @grimos/shared build
```

3. Start the development servers:

```bash
pnpm dev
```

## Automated Migration

For convenience, we've provided migration scripts:

* For Linux/macOS: `./scripts/migrate-to-monorepo.sh`
* For Windows: `scripts\migrate-to-monorepo.bat`

These scripts will:

1. Create the necessary directory structure
2. Move the frontend and backend code to their respective locations
3. Install dependencies
4. Build the shared package

After running the script, you should review the migrated code and make any necessary adjustments.

## Verification

After migration, verify that:

1. The frontend can be started with `pnpm --filter @grimos/frontend dev`
2. The backend can be started with `pnpm --filter @grimos/backend dev`
3. The frontend can communicate with the backend API
4. All tests pass with `pnpm test`

## Troubleshooting

* If you encounter dependency issues, try running `pnpm install` again
* If the shared package isn't being recognized, ensure it's built with `pnpm --filter @grimos/shared build`
* Check environment variables in `.env.local` files to ensure proper configuration
