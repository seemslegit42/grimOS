/**
 * Error handling middleware for API Gateway
 */

function errorHandler(err, req, res, next) {
  console.error('Error:', err)

  // Default error response
  const errorResponse = {
    status: 'error',
    message: 'An unexpected error occurred',
  }

  // Determine response status code
  let statusCode = err.statusCode || 500

  // Handle specific error types
  if (err.name === 'UnauthorizedError') {
    statusCode = 401
    errorResponse.message = 'Unauthorized: Invalid or missing authentication token'
  } else if (err.name === 'ValidationError') {
    statusCode = 400
    errorResponse.message = err.message || 'Validation error'
    errorResponse.details = err.details
  } else if (err.name === 'ServiceUnavailableError') {
    statusCode = 503
    errorResponse.message = 'Service unavailable'
  }

  // Add error stack in development
  if (process.env.NODE_ENV === 'development') {
    errorResponse.stack = err.stack
  }

  res.status(statusCode).json(errorResponse)
}

module.exports = errorHandler
