# gRPC Integration for Microservices

This guide explains how to use gRPC for synchronous communication between microservices in the grimOS platform.

## Overview

The grimOS platform uses gRPC for efficient, type-safe, synchronous communication between microservices. This implementation includes:

1. Protocol Buffer (protobuf) definitions for service APIs
2. Generated Python gRPC server and client code
3. gRPC server implementation in the Auth service
4. gRPC client implementation in the User service
5. Integration with FastAPI endpoints

## Project Structure

```
services/
├── protos/                  # Protocol Buffer definitions
│   ├── auth.proto           # Auth service API definition
│   └── user.proto           # User service API definition
├── auth/                    # Auth service
│   └── app/
│       └── grpc/            # gRPC server implementation
│           ├── __init__.py
│           ├── auth_pb2.py      # Generated code
│           ├── auth_pb2_grpc.py # Generated code
│           └── server.py        # gRPC server implementation
├── user/                    # User service
│   └── app/
│       └── grpc/            # gRPC client implementation
│           ├── __init__.py
│           ├── auth_pb2.py      # Generated code
│           ├── auth_pb2_grpc.py # Generated code
│           ├── user_pb2.py      # Generated code
│           ├── user_pb2_grpc.py # Generated code
│           └── auth_client.py   # gRPC client implementation
└── generate_grpc.sh         # Script to generate gRPC code
```

## Setup Instructions

### 1. Install Dependencies

Both services require the following Python packages:

* `grpcio`
* `grpcio-tools`
* `protobuf`

These are included in the `pyproject.toml` files for both services.

### 2. Generate gRPC Code

Run the provided script to generate Python code from the protobuf definitions:

```bash
cd services
chmod +x generate_grpc.sh
./generate_grpc.sh
```

This will generate the necessary Python files in the `auth/app/grpc/` and `user/app/grpc/` directories.

### 3. Start the Services

Use Docker Compose to start both services:

```bash
cd services
docker-compose up -d
```

## Using gRPC in Your Services

### Defining Service APIs with Protocol Buffers

1. Create a `.proto` file in the `services/protos/` directory
2. Define your service interface and message types
3. Run the `generate_grpc.sh` script to generate code

Example:

```protobuf
syntax = "proto3";

package myservice;

service MyService {
  rpc DoSomething(MyRequest) returns (MyResponse);
}

message MyRequest {
  string input = 1;
}

message MyResponse {
  string output = 1;
  bool success = 2;
}
```

### Implementing a gRPC Server

1. Create a servicer class that inherits from the generated `*Servicer` class
2. Implement the methods defined in your service
3. Start the gRPC server in your application

Example:

```python
class MyServiceServicer(my_pb2_grpc.MyServiceServicer):
    def DoSomething(self, request, context):
        # Implement your logic here
        return my_pb2.MyResponse(
            output=f"Processed: {request.input}",
            success=True
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    return server
```

### Implementing a gRPC Client

1. Create a client class that wraps the generated stub
2. Implement methods to call the remote service
3. Use the client in your application

Example:

```python
class MyServiceClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = my_pb2_grpc.MyServiceStub(self.channel)

    def do_something(self, input_text):
        request = my_pb2.MyRequest(input=input_text)
        try:
            response = self.stub.DoSomething(request)
            return response
        except grpc.RpcError as e:
            print(f"RPC error: {e.details()}")
            return None
```

## Best Practices for Service Discovery and Load Balancing

### Service Discovery

1. **Environment Variables**: Use environment variables to configure service addresses

   ```python
   service_address = os.getenv("MY_SERVICE_ADDRESS", "localhost:50051")
   ```

2. **DNS-based Discovery**: Use service names in Docker Compose or Kubernetes

   ```python
   service_address = "my-service:50051"  # Resolves via DNS
   ```

3. **Service Registry**: For more complex setups, consider using Consul or etcd
   ```python
   # Pseudo-code for service registry lookup
   service_address = registry.lookup("my-service")
   ```

### Load Balancing

1. **Client-side Load Balancing**: Use gRPC's built-in load balancing

   ```python
   channel = grpc.insecure_channel(
       "my-service:50051",
       options=[
           ("grpc.lb_policy_name", "round_robin"),
       ]
   )
   ```

2. **Proxy-based Load Balancing**: Use Envoy or NGINX as a proxy

   ```python
   # Connect to the proxy instead of directly to the service
   channel = grpc.insecure_channel("envoy-proxy:8080")
   ```

3. **Kubernetes Load Balancing**: Use Kubernetes Service resources
   ```python
   # The service name resolves to the Kubernetes service
   channel = grpc.insecure_channel("my-service.namespace:50051")
   ```

## Security Considerations

1. **TLS Encryption**: Use TLS for secure communication

   ```python
   # Server
   server_credentials = grpc.ssl_server_credentials(...)
   server.add_secure_port('[::]:50051', server_credentials)

   # Client
   credentials = grpc.ssl_channel_credentials(...)
   channel = grpc.secure_channel('localhost:50051', credentials)
   ```

2. **Authentication**: Implement token-based authentication

   ```python
   # Client
   metadata = [('authorization', f'Bearer {token}')]
   response = stub.Method(request, metadata=metadata)

   # Server
   def Method(self, request, context):
       metadata = dict(context.invocation_metadata())
       token = metadata.get('authorization')
       # Validate token
   ```

3. **Authorization**: Check permissions in the server implementation
   ```python
   def Method(self, request, context):
       user_id = get_user_id_from_context(context)
       if not has_permission(user_id, 'resource', 'action'):
           context.abort(grpc.StatusCode.PERMISSION_DENIED, 'Not authorized')
   ```

## Troubleshooting

1. **Connection Issues**:

   * Check if the server is running
   * Verify the address and port
   * Check network connectivity and firewall rules

2. **Deadline Exceeded**:

   * Increase timeout settings
   * Check for performance bottlenecks in the server

3. **Protocol Buffer Mismatch**:

   * Ensure both client and server use the same .proto definitions
   * Regenerate code if needed

4. **Debugging**:
   * Enable gRPC logging:
     ```python
     import logging
     logging.basicConfig(level=logging.DEBUG)
     ```
   * Use gRPC reflection for introspection
