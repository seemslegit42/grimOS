/**
 * Service proxy middleware for API Gateway
 */
const { createProxyMiddleware } = require('http-proxy-middleware');

/**
 * Create a proxy middleware for a specific service
 * @param {string} serviceName - The name of the service to proxy to
 * @param {string} serviceUrl - The URL of the service
 * @param {Object} options - Additional proxy options
 * @returns {Function} Proxy middleware
 */
function createServiceProxy(serviceName, serviceUrl, options = {}) {
  console.log(`Creating proxy for ${serviceName} -> ${serviceUrl}`);
  
  // Default proxy options
  const defaultOptions = {
    target: serviceUrl,
    changeOrigin: true,
    pathRewrite: {
      [`^/api/v1/${serviceName}`]: '/api/v1',
    },
    logLevel: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
    onProxyReq: (proxyReq, req, res) => {
      // Add service-specific headers if needed
      proxyReq.setHeader('X-Service', serviceName);
      
      // Add service secret key for inter-service communication
      if (process.env.SERVICE_SECRET_KEY) {
        proxyReq.setHeader('X-Service-Key', process.env.SERVICE_SECRET_KEY);
      }
      
      // Pass user ID if authenticated
      if (req.user && req.user.id) {
        proxyReq.setHeader('X-User-ID', req.user.id);
      }
      
      // Pass user roles if available
      if (req.user && req.user.roles && Array.isArray(req.user.roles)) {
        proxyReq.setHeader('X-User-Roles', req.user.roles.join(','));
      }
      
      // Log the proxied request in development
      if (process.env.NODE_ENV === 'development') {
        console.log(`[Proxy] ${req.method} ${req.url} -> ${serviceUrl}`);
      }
      
      // If request has a body, need to restream it
      if (req.body && Object.keys(req.body).length > 0) {
        const bodyData = JSON.stringify(req.body);
        // Update content-length
        proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
        // Write body to request
        proxyReq.write(bodyData);
      }
    },
    onError: (err, req, res) => {
      console.error(`[Proxy Error] ${serviceName}:`, err);
      res.writeHead(503, {
        'Content-Type': 'application/json',
      });
      res.end(JSON.stringify({
        status: 'error',
        message: `Service ${serviceName} is currently unavailable`,
        error: process.env.NODE_ENV === 'development' ? err.message : undefined,
      }));
    },
    // Add retry logic for failed requests
    onProxyRes: (proxyRes, req, res) => {
      // Add additional response processing if needed
      const statusCode = proxyRes.statusCode;
      
      // Log all 5xx errors
      if (statusCode >= 500) {
        console.error(`[Proxy] Service ${serviceName} returned ${statusCode} for ${req.method} ${req.url}`);
      }
    },
  };

  // Merge default options with provided options
  const proxyOptions = { ...defaultOptions, ...options };
  
  return createProxyMiddleware(proxyOptions);
}
  
  return createProxyMiddleware(proxyOptions);
}

module.exports = {
  createServiceProxy,
};
