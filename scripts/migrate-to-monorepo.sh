#!/bin/bash

# Migration script for converting GrimOS from monolithic to Turborepo structure
# This script should be run from the root of the project

set -e

echo "Starting migration to Turborepo monorepo structure..."

# Create necessary directories if they don't exist
mkdir -p apps/frontend/app
mkdir -p apps/frontend/components
mkdir -p apps/frontend/public
mkdir -p apps/frontend/styles
mkdir -p apps/backend/app
mkdir -p packages/shared/src

# Move Next.js frontend files
echo "Moving Next.js frontend files..."
cp -r app/layout.tsx app/page.tsx apps/frontend/app/
cp -r styles/* apps/frontend/styles/
cp -r components/* apps/frontend/components/
cp -r public/* apps/frontend/public/ 2>/dev/null || true
cp next.config.ts apps/frontend/next.config.js
cp tsconfig.json apps/frontend/
cp postcss.config.js apps/frontend/
cp tailwind.config.js apps/frontend/

# Move FastAPI backend files
echo "Moving FastAPI backend files..."
cp -r app/fastapi-backend/backend/* apps/backend/
cp app/fastapi-backend/backend/app/* apps/backend/app/

# Install dependencies
echo "Installing dependencies..."
pnpm install

# Build shared package
echo "Building shared package..."
pnpm --filter @bitbrew/shared build

echo "Migration completed successfully!"
echo "Please review the new structure in the apps/ and packages/ directories."
echo "You can now run 'pnpm dev' to start the development servers."