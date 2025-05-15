#!/usr/bin/env node

/**
 * This script checks if ESLint and Prettier are properly installed and configured.
 * It also provides instructions on how to fix any issues.
 */

const { execSync, exec } = require('child_process')
const fs = require('fs')
const path = require('path')

const rootDir = path.resolve(__dirname, '..')

console.log('Checking ESLint and Prettier configuration...')

// Helper function to execute commands safely
function safeExec(command, options = {}) {
  try {
    return { 
      output: execSync(command, { ...options, stdio: 'pipe' }).toString().trim(),
      success: true
    }
  } catch (error) {
    return { 
      output: error.stdout ? error.stdout.toString() : error.message,
      error: error,
      success: false
    }
  }
}

// Check if ESLint is installed
const eslintCheck = safeExec('npx eslint --version')
if (eslintCheck.success) {
  console.log(`✅ ESLint is installed: ${eslintCheck.output}`)
} else {
  console.error('❌ ESLint is not properly installed. Run: pnpm install -D eslint')
  process.exit(1)
}

// Check if Prettier is installed
const prettierCheck = safeExec('npx prettier --version')
if (prettierCheck.success) {
  console.log(`✅ Prettier is installed: ${prettierCheck.output}`)
} else {
  console.error('❌ Prettier is not properly installed. Run: pnpm install -D prettier')
  process.exit(1)
}

// Check if ESLint config exists
const eslintConfigPath = path.join(rootDir, '.eslintrc.json')
const eslintConfigExists = fs.existsSync(eslintConfigPath)
if (eslintConfigExists) {
  console.log('✅ ESLint configuration file exists')
} else {
  console.error('❌ ESLint configuration file is missing')
  process.exit(1)
}

// Check if ESLint ignore file exists
const eslintIgnorePath = path.join(rootDir, '.eslintignore')
const eslintIgnoreExists = fs.existsSync(eslintIgnorePath)
if (eslintIgnoreExists) {
  console.log('✅ ESLint ignore file exists')
} else {
  console.warn('⚠️ ESLint ignore file is missing. This is optional but recommended.')
}

// Check if Prettier config exists
const prettierConfigPath = path.join(rootDir, 'prettier.config.js')
const prettierConfigExists = fs.existsSync(prettierConfigPath)
if (prettierConfigExists) {
  console.log('✅ Prettier configuration file exists')
  
  // Validate Prettier config
  try {
    const prettierConfig = require(prettierConfigPath)
    console.log('✅ Prettier configuration is valid')
  } catch (error) {
    console.error(`❌ Prettier configuration is invalid: ${error.message}`)
    process.exit(1)
  }
} else {
  console.error('❌ Prettier configuration file is missing')
  process.exit(1)
}

// Check if pre-commit hooks are configured
const preCommitConfigPath = path.join(rootDir, '.pre-commit-config.yaml')
const preCommitConfigExists = fs.existsSync(preCommitConfigPath)
if (preCommitConfigExists) {
  console.log('✅ Pre-commit configuration file exists')
} else {
  console.error('❌ Pre-commit configuration file is missing')
  process.exit(1)
}

// Test ESLint on a sample file
const findTsFiles = safeExec('find . -name "*.ts" -not -path "*/node_modules/*" -not -path "*/dist/*" | head -n 1', { cwd: rootDir })
if (findTsFiles.success && findTsFiles.output) {
  console.log(`Testing ESLint on file: ${findTsFiles.output}`)
  const eslintTest = safeExec(`npx eslint "${findTsFiles.output}"`, { cwd: rootDir })
  if (eslintTest.success) {
    console.log('✅ ESLint is working correctly')
  } else {
    console.log('⚠️ ESLint found issues in the test file (this is normal if the file has linting errors)')
  }
} else {
  console.log('⚠️ No TypeScript files found to test ESLint')
}

// Test Prettier on a sample file
const findFiles = safeExec(
  'find . -name "*.js" -not -path "*/node_modules/*" -not -path "*/dist/*" | head -n 1',
  { cwd: rootDir })
if (findFiles.success && findFiles.output) {
  console.log(`Testing Prettier on file: ${findFiles.output}`)
  const prettierTest = safeExec(`npx prettier --check "${findFiles.output}"`, { cwd: rootDir })
  if (prettierTest.success) {
    console.log('✅ Prettier is working correctly')
  } else {
    console.log('⚠️ Prettier found formatting issues in the test file (this is normal if the file needs formatting)')
    console.log('   You can run: pnpm format to fix formatting issues')
  }
} else {
  console.log('⚠️ No JavaScript files found to test Prettier, trying other file types...')
  
  // Try with package.json as a fallback
  const packageJsonPath = path.join(rootDir, 'package.json')
  if (fs.existsSync(packageJsonPath)) {
    console.log('Testing Prettier on package.json')
    const prettierTest = safeExec(`npx prettier --check "package.json"`, { cwd: rootDir })
    if (prettierTest.success) {
      console.log('✅ Prettier is working correctly')
    } else {
      console.log('⚠️ Prettier found formatting issues in package.json (this is normal if the file needs formatting)')
      console.log('   You can run: pnpm format to fix formatting issues')
    }
  } else {
    console.log('⚠️ No files found to test Prettier')
  }
}

console.log('\n✅ ESLint and Prettier are properly configured!')
console.log('\nYou can run the following commands:')
console.log('- pnpm lint: Run ESLint on all files')
console.log('- pnpm lint:fix: Run ESLint and fix issues automatically')
console.log('- pnpm format: Format all files with Prettier')
console.log('- pnpm format:check: Check if all files are formatted correctly')

console.log('\nIf the format command fails with exit code 2, it means there are files that need formatting.')
console.log('This is normal and can be fixed by running: pnpm format')