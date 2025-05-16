# grimOS Frontend App Directory

This directory contains the Next.js App Router implementation for the grimOS frontend application.

## Directory Structure

- `app/` - The main Next.js App Router directory
  - `api/` - API routes
  - `dashboard/` - Dashboard pages
  - `landing/` - Landing pages
  - `operations/` - Operations pages
  - `profile/` - User profile pages
  - `sign-in/` - Sign in page
  - `sign-up/` - Sign up page
  - `bitbrew/` - BitBrew specific pages
  - `layout.tsx` - Root layout component
  - `page.tsx` - Root page component
  - `globals.css` - Global CSS styles

## Development Guidelines

1. **Page Components**: All page components should be placed in their respective route directories with the filename `page.tsx`.

2. **Layout Components**: Layout components should be named `layout.tsx` and placed in their respective route directories.

3. **Route Groups**: Use route groups (e.g., `(main)`) to organize routes without affecting the URL structure.

4. **Components**: Reusable components should be placed in the `src/components` directory, not in the `app` directory.

5. **Features**: Feature-specific components and logic should be placed in the `src/features` directory.

6. **API Routes**: API routes should be placed in the `app/api` directory with the filename `route.ts`.

## Important Notes

- The `app` directory is the only directory that should contain Next.js App Router pages and layouts.
- Do not create a duplicate app directory structure in the `src` directory.
- Follow the Next.js App Router conventions for file naming and directory structure.