#!/bin/sh

# Wait for Kong to be available
echo "Waiting for Kong Admin API..."
until curl -s http://kong:8001/status > /dev/null; do
  sleep 5
done

echo "Kong Admin API is available, configuring routes..."

# Add GrimOS API Service
curl -i -X POST http://kong:8001/services \
  --data name=grimos-api \
  --data url=http://backend:8000/api/v1

# Add routes for the GrimOS API
curl -i -X POST http://kong:8001/services/grimos-api/routes \
  --data name=api-route \
  --data 'paths[]=/api/v1' \
  --data 'strip_path=false'

# Add authentication plugin
curl -i -X POST http://kong:8001/services/grimos-api/plugins \
  --data name=jwt \
  --data 'config.secret_is_base64=false' \
  --data 'config.claims_to_verify=exp'

# Add rate limiting plugin
curl -i -X POST http://kong:8001/services/grimos-api/plugins \
  --data name=rate-limiting \
  --data 'config.minute=100' \
  --data 'config.hour=1000' \
  --data 'config.policy=local'

# Add public routes (paths that don't need authentication)
PUBLIC_PATHS="/api/v1/health,/api/v1/auth/login,/api/v1/auth/register,/api/v1/auth/oauth,/metrics"

# Create a separate route for public endpoints
curl -i -X POST http://kong:8001/services/grimos-api/routes \
  --data name=public-api-route \
  --data "paths[]=$PUBLIC_PATHS" \
  --data 'strip_path=false'

# Add CORS plugin
curl -i -X POST http://kong:8001/services/grimos-api/plugins \
  --data name=cors \
  --data 'config.origins=*' \
  --data 'config.methods=GET,POST,PUT,DELETE,OPTIONS' \
  --data 'config.headers=Accept,Accept-Version,Content-Length,Content-MD5,Content-Type,Date,Authorization' \
  --data 'config.exposed_headers=X-Auth-Token' \
  --data 'config.credentials=true' \
  --data 'config.max_age=3600'

echo "Kong configured successfully!"
