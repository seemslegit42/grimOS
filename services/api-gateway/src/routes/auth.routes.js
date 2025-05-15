/**
 * Auth service routes for API Gateway
 */
const express = require('express')
const { createServiceProxy } = require('../middlewares/proxy.middleware')
const authMiddleware = require('../middlewares/auth.middleware')

const router = express.Router()

// Create proxy middleware for the auth service
const authServiceProxy = createServiceProxy('auth', process.env.AUTH_SERVICE_URL || 'http://auth:8000')

// Public routes that don't require authentication
router.post('/login', authServiceProxy)
router.post('/refresh', authServiceProxy)
router.post('/register', authServiceProxy)
router.post('/forgot-password', authServiceProxy)
router.post('/reset-password', authServiceProxy)

// Protected routes that require authentication
router.use('/me', authMiddleware, authServiceProxy)
router.use('/logout', authMiddleware, authServiceProxy)
router.use('/update-password', authMiddleware, authServiceProxy)

// Admin routes - protected and restricted to admin users
router.use('/users', authMiddleware, authServiceProxy)

module.exports = router
