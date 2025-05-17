# Kubernetes and Helm Deployment Guide for Grimoire OS

This guide explains how to containerize and deploy the grimOS microservices stack (including the auth microservice) with Kubernetes and Helm.

## Prerequisites

Before you begin, ensure you have the following installed:

* Docker (v20.10.0+)
* kubectl (v1.24.0+)
* Helm (v3.8.0+)
* Either Minikube or K3s for local development

## Setting Up a Local Kubernetes Cluster

### Option 1: Minikube

```powershell
# Install Minikube (if not already installed)
winget install minikube

# Start Minikube with 4GB RAM and 2 CPUs
minikube start --memory=4096 --cpus=2

# Enable the Ingress addon
minikube addons enable ingress

# Verify Minikube is running
minikube status
```

### Option 2: K3s (using WSL)

```bash
# Install K3s without Traefik (we'll install it separately)
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=traefik" sh -

# Get the kubeconfig file
mkdir -p ~/.kube
sudo cat /etc/rancher/k3s/k3s.yaml > ~/.kube/config
sudo chmod 644 ~/.kube/config
export KUBECONFIG=~/.kube/config
```

## Installing Traefik Ingress Controller

```powershell
# Add the Traefik Helm repository
helm repo add traefik https://helm.traefik.io/traefik
helm repo update

# Install Traefik
helm install traefik traefik/traefik -n kube-system
```

## Building and Pushing Docker Images

First, build the Docker images for each microservice:

```powershell
# Build the auth microservice image
cd services/auth
docker build -t grimoire/auth:latest .

# Build the API Gateway image
cd ../api-gateway
docker build -t grimoire/api-gateway:latest .

# Build the backend image (if applicable)
cd ../../apps/backend
docker build -t grimoire/backend:latest .

# Build the frontend image
cd ../frontend
docker build -t grimoire/frontend:latest .
```

If you're using a container registry (like Docker Hub, GitHub Container Registry, or a private registry):

```powershell
# Log in to your container registry
docker login your-registry.example.com

# Tag and push the images
docker tag grimoire/auth:latest your-registry.example.com/grimoire/auth:latest
docker push your-registry.example.com/grimoire/auth:latest

docker tag grimoire/api-gateway:latest your-registry.example.com/grimoire/api-gateway:latest
docker push your-registry.example.com/grimoire/api-gateway:latest

docker tag grimoire/backend:latest your-registry.example.com/grimoire/backend:latest
docker push your-registry.example.com/grimoire/backend:latest

docker tag grimoire/frontend:latest your-registry.example.com/grimoire/frontend:latest
docker push your-registry.example.com/grimoire/frontend:latest
```

If you're using Minikube for local development, you can load the images directly:

```powershell
# Load images into Minikube
minikube image load grimoire/auth:latest
minikube image load grimoire/api-gateway:latest
minikube image load grimoire/backend:latest
minikube image load grimoire/frontend:latest
```

## Deploying with Helm

### 1. Update Helm Dependencies

```powershell
cd charts/grimoire
helm dependency update
```

### 2. Install the Helm Chart

For development:

```powershell
helm install grimoire . --create-namespace --namespace grimoire-dev
```

For production:

```powershell
# Create a values file for production
$values = @"
global:
  environment: production
  imageRegistry: "your-registry.example.com"
  imagePullSecrets:
    - name: registry-credentials

frontend:
  replicaCount: 2

backend:
  replicaCount: 3

auth:
  replicaCount: 2

apiGateway:
  replicaCount: 2

postgresql:
  primary:
    persistence:
      size: 10Gi
"@

# Write the values to a file
$values | Out-File -FilePath prod-values.yaml

# Install the chart with production values
helm install grimoire . --namespace grimoire-prod --create-namespace -f prod-values.yaml
```

### 3. Check the Deployment Status

```powershell
# Check the pods
kubectl get pods -n grimoire-dev

# Check the services
kubectl get svc -n grimoire-dev

# Check the ingress resources
kubectl get ingress -n grimoire-dev
```

### 4. Access the Application

If you're using Minikube:

```powershell
# Get the Minikube IP
minikube ip

# Add entries to your hosts file for the Ingress hostnames
# Open Notepad as Administrator and edit C:\Windows\System32\drivers\etc\hosts
# Add:
# <minikube-ip> grimoire.local
# <minikube-ip> auth.grimoire.local
```

If you're using K3s:

```bash
# Get the Node IP
kubectl get nodes -o wide

# Add entries to your hosts file:
# <node-ip> grimoire.local
# <node-ip> auth.grimoire.local
```

Then access the application at http://grimoire.local

## Upgrading the Deployment

When you make changes to your application or configuration:

```powershell
# Update the Helm chart
helm upgrade grimoire . --namespace grimoire-dev
```

## Scaling Services

You can scale services manually:

```powershell
# Scale the auth microservice to 3 replicas
kubectl scale deployment grimoire-auth --replicas=3 -n grimoire-dev
```

Or update the values.yaml file and perform a Helm upgrade.

## Autoscaling

To enable autoscaling, update your values.yaml file:

```yaml
auth:
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilizationPercentage: 70
```

Then upgrade your Helm deployment:

```powershell
helm upgrade grimoire . --namespace grimoire-dev
```

## Troubleshooting

### Common Issues and Solutions

1. **Pods stuck in "Pending" state**

   ```powershell
   kubectl describe pod <pod-name> -n grimoire-dev
   ```

   Possible causes:

   * Insufficient resources: Increase Minikube/K3s resources or reduce resource requests.
   * PersistentVolumeClaim issues: Check PVC status and storage class.

2. **Image Pull Errors**

   ```powershell
   kubectl describe pod <pod-name> -n grimoire-dev
   ```

   Possible causes:

   * Incorrect image name or tag: Verify image names in values.yaml.
   * Missing pull secret: Add imagePullSecrets to your values.yaml.

3. **Service unavailable**

   ```powershell
   # Check if service exists
   kubectl get svc -n grimoire-dev

   # Check service endpoints
   kubectl get endpoints -n grimoire-dev
   ```

   Possible causes:

   * Selector not matching pod labels: Check selectors in service definition.
   * Pod not running: Check pod status.

4. **Ingress not working**

   ```powershell
   kubectl describe ingress -n grimoire-dev
   ```

   Possible causes:

   * Ingress controller not installed: Install Traefik or another ingress controller.
   * Incorrect host configuration: Verify hosts in ingress and in your local hosts file.

5. **Database Connection Issues**

   ```powershell
   # Check PostgreSQL pod logs
   kubectl logs <postgres-pod-name> -n grimoire-dev

   # Check auth service logs
   kubectl logs <auth-pod-name> -n grimoire-dev
   ```

   Possible causes:

   * Incorrect database credentials: Check secrets and environment variables.
   * Database not initialized: Wait for initialization to complete.

### Viewing Logs

```powershell
# View logs for a pod
kubectl logs <pod-name> -n grimoire-dev

# Follow logs in real time
kubectl logs -f <pod-name> -n grimoire-dev

# View logs for all pods with a specific label
kubectl logs -l app=auth -n grimoire-dev
```

### Executing Commands in Pods

```powershell
# Get a shell in a pod
kubectl exec -it <pod-name> -n grimoire-dev -- /bin/bash

# Run a command in a pod
kubectl exec <pod-name> -n grimoire-dev -- <command>
```

## Cleaning Up

To remove the deployment:

```powershell
# Delete the Helm release
helm uninstall grimoire -n grimoire-dev

# Delete the namespace
kubectl delete namespace grimoire-dev
```

## Advanced Configuration

### Adding Custom Environment Variables

Update the configMap and secrets sections in your values.yaml file, then upgrade the Helm chart.

### Custom Health Checks

Modify the livenessProbe and readinessProbe sections in your values.yaml file to customize health checks.

### Persistent Storage Configuration

Adjust the persistence section and the PostgreSQL configuration to customize storage settings.

## Security Best Practices

1. **Secrets Management**

   * Never commit secrets to version control
   * Consider using a secrets management tool like HashiCorp Vault or Kubernetes External Secrets

2. **Network Policies**

   * Define network policies to restrict traffic between pods

3. **RBAC (Role-Based Access Control)**

   * Use the principle of least privilege
   * Create specific service accounts for each microservice

4. **Security Contexts**
   * Run containers as non-root users
   * Use read-only file systems where possible

By following this guide, you should be able to successfully containerize and deploy the grimOS microservices stack with Kubernetes and Helm.

## Service Discovery with Kubernetes DNS

Kubernetes provides a built-in DNS service that allows services to discover each other by name within the cluster. This is essential for internal microservice communication in grimOS.

### Configuration

1. **Ensure CoreDNS is Enabled**
   CoreDNS is the default DNS server for Kubernetes. Verify that it is running in your cluster:
   ```bash
   kubectl get pods -n kube-system -l k8s-app=kube-dns
   ```
   You should see pods for CoreDNS running.

2. **Service Naming Convention**
   - Services can be accessed using the format: `<service-name>.<namespace>.svc.cluster.local`
   - For example, a service named `auth-service` in the `default` namespace can be accessed as:
     ```
     auth-service.default.svc.cluster.local
     ```

3. **DNS Policy**
   Ensure that pods have the correct DNS policy. By default, pods inherit the cluster's DNS settings. You can explicitly set the DNS policy in your pod or deployment spec:
   ```yaml
   spec:
     dnsPolicy: ClusterFirst
   ```

4. **Testing Service Discovery**
   Use the `nslookup` or `dig` command within a pod to test DNS resolution:
   ```bash
   kubectl exec -it <pod-name> -- nslookup auth-service.default.svc.cluster.local
   ```

### Example Usage in grimOS

- All grimOS microservices should use Kubernetes DNS for internal communication.
- Ensure that service names are unique within their namespace.
- Use environment variables or configuration files to store service names for easy updates.

### Troubleshooting

- If DNS resolution fails, check the CoreDNS logs:
  ```bash
  kubectl logs -n kube-system -l k8s-app=kube-dns
  ```
- Verify that the service and pod names are correct.
- Ensure network policies are not blocking DNS traffic.

By following these steps, you can ensure reliable service discovery for all grimOS microservices.

## Private Docker Registry Integration

To use a private Docker registry with Kubernetes, follow these steps:

1. **Create a Docker Registry Secret**
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=${DOCKER_REGISTRY_URL} \
     --docker-username=${DOCKER_REGISTRY_USERNAME} \
     --docker-password=${DOCKER_REGISTRY_PASSWORD} \
     --docker-email=${DOCKER_REGISTRY_EMAIL}
   ```

2. **Reference the Secret in Your Deployment**
   Add the following to your Kubernetes deployment YAML:
   ```yaml
   spec:
     imagePullSecrets:
       - name: regcred
   ```

3. **Update Image References**
   Ensure all image references include the private registry URL, e.g., `${DOCKER_REGISTRY_URL}/grimos-backend:latest`.

By following these steps, you can securely pull images from the private Docker registry.
