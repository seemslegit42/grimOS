# Frontend Dockerfile
# Stage 1: Build the React (Vite) application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copy source code and build the application
COPY . .
RUN pnpm run build

# Stage 2: Serve the application with Nginx
FROM nginx:1.23-alpine

# Copy built assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration if needed
# Uncomment and modify the following line if you have a custom nginx.conf
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
