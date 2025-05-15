require('dotenv').config()
const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const morgan = require('morgan')
const rateLimit = require('express-rate-limit')

// Import routes
const authRoutes = require('./routes/auth.routes')
const userRoutes = require('./routes/users.routes')

// Import middlewares
const errorHandler = require('./middlewares/error.middleware')

// Create Express app
const app = express()

// Set up middleware
app.use(helmet()) // Security headers
app.use(express.json()) // Parse JSON bodies

// Configure CORS
const corsOptions = {
  origin: process.env.CORS_ORIGIN?.split(',') || ['http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
}
app.use(cors(corsOptions))

// Request logging
app.use(morgan('combined'))

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 60 * 1000, // 1 minute
  max: parseInt(process.env.RATE_LIMIT_MAX) || 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
})
app.use(limiter)

// Define routes
app.use('/api/v1/auth', authRoutes)
app.use('/api/v1/users', userRoutes)

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    service: 'API Gateway',
    timestamp: new Date().toISOString(),
  })
})

// Error handling middleware (should be last)
app.use(errorHandler)

// Start the server
const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
  console.log(`API Gateway listening on port ${PORT}`)
})

module.exports = app // For testing
