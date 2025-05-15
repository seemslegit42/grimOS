# Grimoire OS Microservices Helm Charts

This directory contains Helm charts for deploying the Grimoire OS microservices stack to Kubernetes.

## Charts Structure

* `charts/grimoire/`
  * Main umbrella chart that includes all services
* `charts/grimoire-frontend/`
  * Frontend Next.js application
* `charts/grimoire-backend/`
  * Backend service (monolithic FastAPI)
* `charts/grimoire-auth/`
  * Authentication microservice
* `charts/grimoire-api-gateway/`
  * API Gateway service

## Prerequisites

* Kubernetes cluster (local or remote)
* Helm 3.x installed
* kubectl configured to communicate with your cluster

## Installation

### 1. Add values.yaml overrides (if needed)

Create a `my-values.yaml` file to override default values:

```yaml
# Example overrides
global:
  environment: production
  imageRegistry: your-registry.io

frontend:
  replicaCount: 2
  resources:
    limits:
      cpu: 500m
      memory: 512Mi

auth:
  replicaCount: 2
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
```

### 2. Install the chart

```bash
helm install grimoire ./charts/grimoire -f my-values.yaml
```

## Uninstallation

```bash
helm uninstall grimoire
```

## Development

For local development with Minikube or K3s, set the `global.environment` to `development`.
