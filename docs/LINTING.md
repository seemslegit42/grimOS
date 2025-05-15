# Linting and Formatting Guide

This project uses ESLint for linting and Prettier for code formatting to ensure consistent code style across the codebase.

## ESLint

ESLint is configured to enforce code quality and catch potential issues in JavaScript and TypeScript files.

### Configuration

- The ESLint configuration is defined in `.eslintrc.json` in the root of the project.
- It extends recommended configurations for TypeScript and import ordering.
- Custom rules are defined to enforce consistent code style.
- Files to ignore are specified in `.eslintignore`.

### Commands

- `pnpm lint`: Run ESLint on all files (via Turbo)
- `pnpm lint:fix`: Run ESLint and automatically fix issues where possible

## Prettier

Prettier is used for consistent code formatting across all files.

### Configuration

- The Prettier configuration is defined in `prettier.config.js` in the root of the project.
- It's configured to use single quotes, 2 spaces for indentation, and other formatting rules.

### Commands

- `pnpm format`: Format all files with Prettier
- `pnpm format:check`: Check if all files are formatted correctly
- `pnpm format:fix-all`: Run a script to format all files in the repository

## Pre-commit Hooks

Pre-commit hooks are configured to run ESLint and Prettier before each commit to ensure that all committed code meets the standards.

### Configuration

- The pre-commit hooks are defined in `.pre-commit-config.yaml` in the root of the project.
- They run ESLint and Prettier on staged files before each commit.

## VSCode Integration

VSCode is configured to use ESLint and Prettier for real-time linting and formatting.

### Configuration

- The VSCode configuration is defined in `.vscode/settings.json`.
- It's configured to format files on save and show ESLint errors in real-time.

### Required Extensions

- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

## Troubleshooting

### ESLint Issues

If you encounter ESLint issues, try the following:

1. Run `pnpm lint:fix` to automatically fix issues
2. Check the ESLint configuration in `.eslintrc.json`
3. Run `pnpm check-tools` to verify the ESLint setup

### Prettier Issues

If you encounter Prettier issues, try the following:

1. Run `pnpm format` to format all files
2. Check the Prettier configuration in `prettier.config.js`
3. Run `pnpm check-tools` to verify the Prettier setup

### Exit Code 2 from Prettier

If Prettier exits with code 2, it means there are files that need formatting. This is normal and can be fixed by running:

```bash
pnpm format
```

## CI/CD Integration

ESLint and Prettier checks are run in the CI/CD pipeline to ensure that all code meets the standards before it's merged.

The GitHub workflow is defined in `.github/workflows/lint-and-format.yml`.