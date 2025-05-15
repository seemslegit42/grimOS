#!/bin/bash

# Script to generate gRPC code from protobuf files

# Set the base directory
BASE_DIR=$(dirname "$0")
PROTO_DIR="$BASE_DIR/protos"
AUTH_SERVICE_DIR="$BASE_DIR/auth/app/grpc"
USER_SERVICE_DIR="$BASE_DIR/user/app/grpc"

# Create the output directories if they don't exist
mkdir -p "$AUTH_SERVICE_DIR"
mkdir -p "$USER_SERVICE_DIR"

# Create __init__.py files to make the directories Python packages
touch "$AUTH_SERVICE_DIR/__init__.py"
touch "$USER_SERVICE_DIR/__init__.py"

echo "Generating gRPC code for auth service..."
# Generate Python code for auth service
python -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$AUTH_SERVICE_DIR" \
    --grpc_python_out="$AUTH_SERVICE_DIR" \
    "$PROTO_DIR/auth.proto" \
    "$PROTO_DIR/user.proto"

echo "Generating gRPC code for user service..."
# Generate Python code for user service
python -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$USER_SERVICE_DIR" \
    --grpc_python_out="$USER_SERVICE_DIR" \
    "$PROTO_DIR/auth.proto" \
    "$PROTO_DIR/user.proto"

echo "Fixing imports in generated files..."
# Fix imports in generated files for auth service
sed -i 's/import auth_pb2 as auth__pb2/import app.grpc.auth_pb2 as auth__pb2/g' "$AUTH_SERVICE_DIR/auth_pb2_grpc.py"
sed -i 's/import user_pb2 as user__pb2/import app.grpc.user_pb2 as user__pb2/g' "$AUTH_SERVICE_DIR/user_pb2_grpc.py"

# Fix imports in generated files for user service
sed -i 's/import auth_pb2 as auth__pb2/import app.grpc.auth_pb2 as auth__pb2/g' "$USER_SERVICE_DIR/auth_pb2_grpc.py"
sed -i 's/import user_pb2 as user__pb2/import app.grpc.user_pb2 as user__pb2/g' "$USER_SERVICE_DIR/user_pb2_grpc.py"

echo "Setting file permissions..."
# Make the generated files executable
chmod -R 644 "$AUTH_SERVICE_DIR"/*.py
chmod -R 644 "$USER_SERVICE_DIR"/*.py

echo "gRPC code generation completed successfully!"

# Print instructions for next steps
echo ""
echo "Next steps:"
echo "1. Start the services with 'docker-compose up -d'"
echo "2. Test the gRPC communication with the health check endpoints:"
echo "   - Auth service: http://localhost:8000/api/v1/profile/health/user-service"
echo "   - User service: http://localhost:8001/api/v1/health/auth-service"