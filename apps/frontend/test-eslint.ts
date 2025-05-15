// This is a test file for ESLint
const testVariable = 'test'
console.log(testVariable)

// Intentional ESLint issue - unused variable
const unusedVar = 'This should trigger an ESLint warning'

// Missing semicolon
const missingStatement = 'This should also trigger an ESLint warning'

// Function with no return type
function testFunction(param) {
  return param
}

export { testFunction }
