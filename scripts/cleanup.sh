#!/bin/bash

# Cleanup script to remove unused files after migration to Turborepo
# This script should be run from the root of the project

set -e

echo "Starting cleanup of unused files..."

# Remove original Next.js files from root
echo "Removing original Next.js files..."
rm -rf instrumentation.ts
rm -rf next.config.ts
rm -rf report-bundle-size.js
rm -rf jest.setup.js
rm -rf next-env.d.ts
rm -rf postcss.config.js
rm -rf styles
rm -rf components
rm -rf e2e
rm -rf lp-items.tsx
rm -rf eslint.config.mjs
rm -rf env.mjs
rm -rf reset.d.ts
rm -rf .storybook
rm -rf playwright.config.ts
rm -rf jest.config.js

# Remove original FastAPI backend
echo "Removing original FastAPI backend..."
rm -rf app

# Remove empty or unused directories
echo "Removing empty or unused directories..."
rm -rf apps/api
rm -rf apps/web
rm -rf packages/ui
rm -rf packages/config

# Remove .next directory (will be regenerated on build)
echo "Removing .next directory..."
rm -rf .next

echo "Cleanup completed successfully!"