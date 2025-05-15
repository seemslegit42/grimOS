/**
 * Admin middleware for API Gateway
 * Restricts access to admin-only routes
 */

function adminMiddleware(req, res, next) {
  try {
    // Ensure user is authenticated
    if (!req.user) {
      return res.status(401).json({
        status: 'error',
        message: 'Unauthorized: Authentication required',
      })
    }

    // Check if user has admin role
    const hasAdminRole = req.user.roles && (req.user.roles.includes('admin') || req.user.roles.includes('superadmin'))

    // Check if user has admin permission
    const hasAdminPermission =
      req.user.permissions &&
      (req.user.permissions.includes('admin:*') || req.user.permissions.includes('users:manage'))

    if (!hasAdminRole && !hasAdminPermission) {
      return res.status(403).json({
        status: 'error',
        message: 'Forbidden: Insufficient permissions',
      })
    }

    // User has admin privileges, proceed
    next()
  } catch (error) {
    console.error('Admin middleware error:', error)
    next(error)
  }
}

module.exports = adminMiddleware
