#!/usr/bin/env node

/**
 * This script formats all files in the repository using Prettier.
 * It's useful for fixing formatting issues in bulk.
 */

const { execSync } = require('child_process')
const path = require('path')

const rootDir = path.resolve(__dirname, '..')

console.log('Formatting all files in the repository...')

try {
  // Format all files using Prettier
  execSync('npx prettier --write "**/*.{ts,tsx,md,js,jsx,json,css,scss}"', { 
    cwd: rootDir,
    stdio: 'inherit'
  })
  
  console.log('\n✅ All files have been formatted successfully!')
} catch (error) {
  console.error('\n❌ Error formatting files:', error.message)
  process.exit(1)
}

console.log('\nYou can now commit the changes.')