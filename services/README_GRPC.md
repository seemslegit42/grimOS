# gRPC Integration Guide for grimOS Microservices

This guide provides detailed instructions for implementing and using gRPC for inter-service communication in the grimOS platform.

## Overview

The grimOS platform uses gRPC for efficient, type-safe, synchronous communication between microservices. This implementation includes:

1. Protocol Buffer (protobuf) definitions for service APIs
2. Generated Python gRPC server and client code
3. gRPC server implementations in each service
4. gRPC client implementations for cross-service communication
5. Integration with FastAPI endpoints

## Project Structure

```
services/
├── protos/                  # Protocol Buffer definitions
│   ├── auth.proto           # Auth service API definition
│   └── user.proto           # User service API definition
├── auth/                    # Auth service
│   └── app/
│       └── grpc/            # gRPC server and client implementation
│           ├── __init__.py
│           ├── auth_pb2.py      # Generated code
│           ├── auth_pb2_grpc.py # Generated code
│           ├── user_pb2.py      # Generated code
│           ├── user_pb2_grpc.py # Generated code
│           ├── server.py        # gRPC server implementation
│           └── user_client.py   # User service client
├── user/                    # User service
│   └── app/
│       └── grpc/            # gRPC server and client implementation
│           ├── __init__.py
│           ├── auth_pb2.py      # Generated code
│           ├── auth_pb2_grpc.py # Generated code
│           ├── user_pb2.py      # Generated code
│           ├── user_pb2_grpc.py # Generated code
│           ├── server.py        # gRPC server implementation
│           └── auth_client.py   # Auth service client
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

## Testing the gRPC Integration

You can test the gRPC integration using the health check endpoints:

1. Auth service health check for User service:

   ```
   GET http://localhost:8000/api/v1/profile/health/user-service
   ```

2. User service health check for Auth service:
   ```
   GET http://localhost:8001/api/v1/health/auth-service
   ```

## Using gRPC in Your Services

### Defining Service APIs with Protocol Buffers

1. Create or update a `.proto` file in the `services/protos/` directory
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

### Dependency Injection with FastAPI

Use FastAPI's dependency injection system to provide gRPC clients to your endpoints:

```python
def get_my_service_client() -> Generator[MyServiceClient, None, None]:
    client = MyServiceClient("my-service:50051")
    try:
        yield client
    finally:
        client.close()

@router.get("/example")
async def example_endpoint(
    client: MyServiceClient = Depends(get_my_service_client)
):
    response = client.do_something("test")
    return {"result": response.output}
```

## Best Practices

### Error Handling

Always handle gRPC errors properly:

```python
try:
    response = stub.Method(request)
    return response
except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.NOT_FOUND:
        # Handle not found
    elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        # Handle timeout
    else:
        # Handle other errors
    return None
```

### Timeouts

Set appropriate timeouts for gRPC calls:

```python
try:
    response = stub.Method(request, timeout=5.0)  # 5 seconds timeout
except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        # Handle timeout
```

### Retries

Implement retry logic for transient failures:

```python
def call_with_retry(method, request, max_retries=3, delay=0.5):
    retries = 0
    while retries < max_retries:
        try:
            return method(request)
        except grpc.RpcError as e:
            if e.code() in [grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED]:
                retries += 1
                if retries < max_retries:
                    time.sleep(delay)
                    continue
            raise
```

### Connection Pooling

Use a single channel for multiple calls to the same service:

```python
class ServiceClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub1 = service1_pb2_grpc.Service1Stub(self.channel)
        self.stub2 = service2_pb2_grpc.Service2Stub(self.channel)
```

### Secure Communication

For production, use TLS for secure communication:

```python
# Server
server_credentials = grpc.ssl_server_credentials(...)
server.add_secure_port('[::]:50051', server_credentials)

# Client
credentials = grpc.ssl_channel_credentials(...)
channel = grpc.secure_channel('localhost:50051', credentials)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: If you see import errors in the generated code, run the `generate_grpc.sh` script again.

2. **Connection Refused**: Check if the gRPC server is running and the port is accessible.

3. **Deadline Exceeded**: Increase the timeout or check if the server is overloaded.

4. **Service Unavailable**: Check if the service is running and healthy.

### Debugging

Enable gRPC logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Use the health check endpoints to verify connectivity between services.

## Further Reading

* [gRPC Documentation](https://grpc.io/docs/)
* [Protocol Buffers Language Guide](https://developers.google.com/protocol-buffers/docs/proto3)
* [gRPC Python API](https://grpc.github.io/grpc/python/)
