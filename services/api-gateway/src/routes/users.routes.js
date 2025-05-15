/**
 * User management routes for API Gateway
 */
const express = require('express')
const { createServiceProxy } = require('../middlewares/proxy.middleware')
const authMiddleware = require('../middlewares/auth.middleware')
const adminMiddleware = require('../middlewares/admin.middleware')

const router = express.Router()

// Create proxy middleware for the auth service
const authServiceProxy = createServiceProxy('auth', process.env.AUTH_SERVICE_URL || 'http://auth:8000')

// Get current user profile
router.get('/me', authMiddleware, authServiceProxy)

// Update current user profile
router.put('/me', authMiddleware, authServiceProxy)

// Admin-only routes for user management
router.get('/', authMiddleware, adminMiddleware, authServiceProxy)
router.get('/:id', authMiddleware, adminMiddleware, authServiceProxy)
router.post('/', authMiddleware, adminMiddleware, authServiceProxy)
router.put('/:id', authMiddleware, adminMiddleware, authServiceProxy)
router.delete('/:id', authMiddleware, adminMiddleware, authServiceProxy)

// User roles and permissions management (admin only)
router.get('/:id/roles', authMiddleware, adminMiddleware, authServiceProxy)
router.put('/:id/roles', authMiddleware, adminMiddleware, authServiceProxy)
router.get('/:id/permissions', authMiddleware, adminMiddleware, authServiceProxy)
router.put('/:id/permissions', authMiddleware, adminMiddleware, authServiceProxy)

module.exports = router
