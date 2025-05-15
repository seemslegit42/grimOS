/**
 * Authentication middleware for API Gateway
 */
const { jwtVerify } = require('jose')
const axios = require('axios')
const { createRemoteJWKSet } = require('jose')

// Auth service URL from environment variables
const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://grimoire-auth:8000'

// Create a JWKS client for verifying tokens
const JWKS_URL = `${AUTH_SERVICE_URL}/.well-known/jwks.json`
let remoteJWKSet

try {
  remoteJWKSet = createRemoteJWKSet(new URL(JWKS_URL))
} catch (error) {
  console.error('Failed to create JWKS client:', error)
}

/**
 * Verify JWT token
 * @param {string} token - JWT token to verify
 * @returns {Promise<Object>} - Decoded token payload
 */
async function verifyToken(token) {
  try {
    // First try to verify with JWKS (if available)
    if (remoteJWKSet) {
      try {
        const { payload } = await jwtVerify(token, remoteJWKSet, {
          issuer: 'grimoireOS',
          audience: 'api-gateway',
        })
        return payload
      } catch (jwksError) {
        console.warn('JWKS verification failed, falling back to secret key:', jwksError.message)
      }
    }

    // Fallback to secret key verification
    const encoder = new TextEncoder()
    const { payload } = await jwtVerify(token, encoder.encode(process.env.JWT_SECRET_KEY))
    return payload
  } catch (error) {
    throw new Error(`Token verification failed: ${error.message}`)
  }
}

/**
 * Validate token with auth service
 * @param {string} token - JWT token to validate
 * @returns {Promise<boolean>} - Whether the token is valid
 */
async function validateTokenWithAuthService(token) {
  try {
    const response = await axios.post(
      `${AUTH_SERVICE_URL}/api/v1/auth/validate-token`,
      { token },
      {
        headers: {
          'Content-Type': 'application/json',
          'X-Service-Key': process.env.SERVICE_SECRET_KEY,
        },
        timeout: 5000, // 5 second timeout
      }
    )
    return response.data.valid === true
  } catch (error) {
    console.error('Token validation with auth service failed:', error.message)
    // If auth service is down, fall back to local validation
    return true
  }
}

/**
 * Main authentication middleware
 */
async function authMiddleware(req, res, next) {
  try {
    // Get authorization header
    const authHeader = req.headers.authorization

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        status: 'error',
        message: 'Unauthorized: Missing or invalid authorization token',
      })
    }

    // Extract token
    const token = authHeader.split(' ')[1]

    if (!token) {
      return res.status(401).json({
        status: 'error',
        message: 'Unauthorized: Missing token',
      })
    }

    try {
      // Verify token
      const payload = await verifyToken(token)

      // Check if token is an access token
      if (payload.type !== 'access') {
        return res.status(401).json({
          status: 'error',
          message: 'Unauthorized: Invalid token type',
        })
      }

      // Check token expiration
      const now = Math.floor(Date.now() / 1000)
      if (payload.exp && payload.exp < now) {
        return res.status(401).json({
          status: 'error',
          message: 'Unauthorized: Token expired',
        })
      }

      // Optional: Validate token with auth service
      if (process.env.VALIDATE_WITH_AUTH_SERVICE === 'true') {
        const isValid = await validateTokenWithAuthService(token)
        if (!isValid) {
          return res.status(401).json({
            status: 'error',
            message: 'Unauthorized: Token revoked or invalid',
          })
        }
      }

      // Attach user information to request
      req.user = {
        id: payload.sub,
        roles: payload.roles || [],
        permissions: payload.permissions || [],
        exp: payload.exp,
        type: payload.type,
      }

      next()
    } catch (error) {
      console.error('Token verification error:', error)
      return res.status(401).json({
        status: 'error',
        message: 'Unauthorized: Invalid token',
      })
    }
  } catch (error) {
    console.error('Authentication middleware error:', error)
    next(error)
  }
}

module.exports = authMiddleware
