#!/bin/bash
# grimOS Infrastructure Deployment Script
# This script manages the deployment of the grimOS infrastructure components

set -e

# Configuration
NAMESPACE_BACKEND="grimos"
NAMESPACE_MONITORING="monitoring"
NAMESPACE_API_GATEWAY="api-gateway"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${GREEN}==== $1 ====${NC}\n"
}

print_step() {
    echo -e "${YELLOW}-> $1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is required but not installed. Please install it and try again."
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking prerequisites"
    check_command kubectl
    check_command helm
    check_command docker
    
    # Check Kubernetes connection
    print_step "Checking Kubernetes connection"
    if ! kubectl cluster-info &> /dev/null; then
        print_error "Cannot connect to Kubernetes cluster. Please ensure your kubeconfig is correctly set up."
        exit 1
    fi
    
    echo -e "${GREEN}All prerequisites satisfied.${NC}"
}

# Create namespaces
create_namespaces() {
    print_header "Creating namespaces"
    
    print_step "Creating namespace: $NAMESPACE_BACKEND"
    kubectl create namespace $NAMESPACE_BACKEND --dry-run=client -o yaml | kubectl apply -f -
    
    print_step "Creating namespace: $NAMESPACE_MONITORING"
    kubectl create namespace $NAMESPACE_MONITORING --dry-run=client -o yaml | kubectl apply -f -
    
    print_step "Creating namespace: $NAMESPACE_API_GATEWAY"
    kubectl create namespace $NAMESPACE_API_GATEWAY --dry-run=client -o yaml | kubectl apply -f -
}

# Deploy monitoring stack
deploy_monitoring() {
    print_header "Deploying monitoring stack"
    
    print_step "Deploying Prometheus and Grafana"
    helm upgrade --install monitoring-stack ./charts/monitoring-stack \
        --namespace $NAMESPACE_MONITORING \
        --set grafana.adminPassword="${GRAFANA_ADMIN_PASSWORD:-admin}" \
        --set environment="${ENVIRONMENT:-production}"
        
    print_step "Waiting for Prometheus and Grafana to be ready"
    kubectl -n $NAMESPACE_MONITORING wait --for=condition=ready pod -l app=prometheus --timeout=120s || true
    kubectl -n $NAMESPACE_MONITORING wait --for=condition=ready pod -l app=grafana --timeout=120s || true
}

# Deploy API Gateway
deploy_api_gateway() {
    print_header "Deploying API Gateway"
    
    print_step "Deploying Kong API Gateway"
    helm upgrade --install api-gateway ./charts/api-gateway \
        --namespace $NAMESPACE_API_GATEWAY \
        --set environment="${ENVIRONMENT:-production}"
        
    print_step "Waiting for API Gateway to be ready"
    kubectl -n $NAMESPACE_API_GATEWAY wait --for=condition=ready pod -l app=kong --timeout=120s || true
}

# Deploy GrimOS backend
deploy_backend() {
    print_header "Deploying GrimOS Backend"
    
    print_step "Building and pushing Docker image"
    if [ -n "$CI" ]; then
        # CI environment - skip build as it's handled by CI pipeline
        print_step "Skipping Docker build in CI environment"
    else
        # Local development - build and load into kind cluster if applicable
        if kubectl config current-context | grep -q "kind"; then
            print_step "Building Docker image for kind cluster"
            docker build -t grimos/backend:latest ./apps/backend
            kind load docker-image grimos/backend:latest
        else
            print_step "Building and pushing Docker image"
            docker build -t grimos/backend:latest ./apps/backend
            docker push grimos/backend:latest
        fi
    fi
    
    print_step "Deploying GrimOS Backend"
    helm upgrade --install grimos-backend ./charts/grimos-backend \
        --namespace $NAMESPACE_BACKEND \
        --set image.tag="${IMAGE_TAG:-latest}" \
        --set environment="${ENVIRONMENT:-production}" \
        --set redis.enabled=true \
        --set postgresql.enabled=true
        
    print_step "Waiting for backend to be ready"
    kubectl -n $NAMESPACE_BACKEND wait --for=condition=ready pod -l app=grimos-backend --timeout=180s || true
}

# Main deployment function
deploy_all() {
    check_prerequisites
    create_namespaces
    deploy_monitoring
    deploy_api_gateway
    deploy_backend
    
    print_header "Deployment Complete"
    print_step "GrimOS Backend: http://backend.${DOMAIN:-localhost}/api/v1"
    print_step "Grafana: http://grafana.${DOMAIN:-localhost}"
    print_step "Prometheus: http://prometheus.${DOMAIN:-localhost}"
    print_step "API Gateway: http://api.${DOMAIN:-localhost}"
}

# Display help
show_help() {
    echo "GrimOS Infrastructure Deployment Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  all             Deploy full infrastructure (monitoring, API gateway, backend)"
    echo "  monitoring      Deploy only monitoring stack"
    echo "  api-gateway     Deploy only API gateway"
    echo "  backend         Deploy only GrimOS backend"
    echo "  clean           Remove all resources"
    echo "  help            Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  ENVIRONMENT     Deployment environment (default: production)"
    echo "  DOMAIN          Base domain for services (default: localhost)"
    echo "  IMAGE_TAG       Docker image tag for backend (default: latest)"
    echo "  GRAFANA_ADMIN_PASSWORD  Grafana admin password (default: admin)"
}

# Clean up all resources
clean_all() {
    print_header "Cleaning up all resources"
    
    print_step "Deleting GrimOS Backend"
    helm uninstall grimos-backend --namespace $NAMESPACE_BACKEND || true
    
    print_step "Deleting API Gateway"
    helm uninstall api-gateway --namespace $NAMESPACE_API_GATEWAY || true
    
    print_step "Deleting Monitoring Stack"
    helm uninstall monitoring-stack --namespace $NAMESPACE_MONITORING || true
    
    print_step "Deleting namespaces"
    kubectl delete namespace $NAMESPACE_BACKEND || true
    kubectl delete namespace $NAMESPACE_API_GATEWAY || true
    kubectl delete namespace $NAMESPACE_MONITORING || true
    
    print_header "Cleanup Complete"
}

# Parse command
case "$1" in
    all)
        deploy_all
        ;;
    monitoring)
        check_prerequisites
        create_namespaces
        deploy_monitoring
        ;;
    api-gateway)
        check_prerequisites
        create_namespaces
        deploy_api_gateway
        ;;
    backend)
        check_prerequisites
        create_namespaces
        deploy_backend
        ;;
    clean)
        clean_all
        ;;
    help|*)
        show_help
        ;;
esac
