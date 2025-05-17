# API Gateway for GrimOS

This directory contains the Kubernetes Helm chart for deploying Kong as an API Gateway for the GrimOS platform.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Plugins](#plugins)
6. [Security](#security)
7. [Monitoring](#monitoring)

## Overview

The API Gateway acts as the entry point to the GrimOS microservices architecture. It handles:

- Request routing
- Authentication
- Rate limiting
- Monitoring
- CORS
- SSL termination

## Architecture

The API Gateway architecture consists of:

1. **Kong** - High-performance API Gateway based on NGINX
2. **Declarative Configuration** - Using DB-less mode for simplicity and GitOps compatibility
3. **Service Discovery** - Kubernetes-based service discovery
4. **Ingress Controller** - External traffic is directed to Kong via Kubernetes Ingress

## Installation

### Prerequisites

- Kubernetes cluster (v1.19+)
- Helm 3.0+
- kubectl configured to communicate with your cluster

### Install the Chart

```bash
# Add the Helm repository
helm repo add kong https://charts.konghq.com
helm repo update

# Install the chart
helm install kong kong/kong -n api-gateway --create-namespace -f values.yaml
```

### Verify Installation

```bash
kubectl get pods -n api-gateway
kubectl get svc -n api-gateway
```

## Configuration

### Basic Configuration

The default configuration is stored in `values.yaml`:

- Kong runs in DB-less mode
- Configuration is loaded from a ConfigMap
- Metrics are exposed for Prometheus scraping

### Custom Configuration

To customize the configuration:

1. Edit the `kong.yml` in the ConfigMap
2. Apply the changes with `kubectl apply -f kong-config.yaml`
3. Restart Kong pods to apply the changes

## Plugins

The following Kong plugins are enabled:

### Authentication

- JWT Authentication for protected routes
- Support for multiple auth providers (OAuth, API Key)

### Traffic Control

- Rate Limiting to prevent abuse
- Response Transformation for consistent API responses
- Request Termination for unavailable services

### Monitoring

- Prometheus metrics for request statistics
- Logging of API access and errors

### Security

- IP Restriction for admin API
- CORS for browser clients

## Security

### JWT Authentication

JWT authentication is configured for most API endpoints. The configuration includes:

- Token validation
- Claims verification
- Role-based access control integration

### API Key Authentication

For service-to-service communication, API Key authentication is available:

- Key provisioning through the admin API
- Key rotation policies
- Scope-based restrictions

## Monitoring

### Prometheus Integration

Kong exposes metrics at the `/metrics` endpoint, which are scraped by Prometheus.

Key metrics include:

- Request count by service/route
- Latency by service/route
- HTTP status code distribution
- Connection counts

### Grafana Dashboard

A Grafana dashboard for Kong metrics is available in the monitoring stack:

- Real-time traffic visualization
- Error rate monitoring
- Latency tracking
- Rate limit usage

## Troubleshooting

### Common Issues

1. **Kong not starting**: Check configuration syntax with `kong check /etc/kong/kong.yml`
2. **JWT validation failing**: Verify JWT configuration and token expiry
3. **Rate limiting too aggressive**: Adjust rate limit configuration in `kong.yml`

### Logs

Access logs for troubleshooting:

```bash
kubectl logs -f deployment/kong -n api-gateway
```
