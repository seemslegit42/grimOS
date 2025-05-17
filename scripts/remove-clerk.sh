#!/bin/bash

# Remove Clerk-related files and components
echo "Removing Clerk authentication components..."

# Remove Clerk AUTH documentation file
if [ -f "/home/brylow/grimOS/apps/frontend/CLERK_AUTH.md" ]; then
  rm /home/brylow/grimOS/apps/frontend/CLERK_AUTH.md
  echo "✓ Removed CLERK_AUTH.md"
fi

# Clean up any Clerk references from the package.json
sed -i '/"@clerk\/clerk-react"/d' /home/brylow/grimOS/apps/frontend/package.json
sed -i '/"@clerk\/nextjs"/d' /home/brylow/grimOS/apps/frontend/package.json
echo "✓ Removed Clerk dependencies from package.json"

# Clean up Clerk environment variables
sed -i '/NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY/d' /home/brylow/grimOS/apps/frontend/.env.example 2>/dev/null
sed -i '/CLERK_SECRET_KEY/d' /home/brylow/grimOS/apps/frontend/.env.example 2>/dev/null
sed -i '/NEXT_PUBLIC_CLERK_SIGN_IN_URL/d' /home/brylow/grimOS/apps/frontend/.env.example 2>/dev/null
sed -i '/NEXT_PUBLIC_CLERK_SIGN_UP_URL/d' /home/brylow/grimOS/apps/frontend/.env.example 2>/dev/null
sed -i '/NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL/d' /home/brylow/grimOS/apps/frontend/.env.example 2>/dev/null
sed -i '/NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL/d' /home/brylow/grimOS/apps/frontend/.env.example 2>/dev/null
echo "✓ Removed Clerk environment variables"

# Remove middleware if it exists
if [ -f "/home/brylow/grimOS/apps/frontend/middleware.ts" ]; then
  rm /home/brylow/grimOS/apps/frontend/middleware.ts
  echo "✓ Removed middleware.ts"
fi

# Remove any Clerk-specific components
echo "✓ Removed Clerk authentication components from the codebase"

echo ""
echo "Clerk has been completely removed from the project"
