#!/usr/bin/env python3
"""
Test script for gRPC communication between Auth and User services.

This script demonstrates how to use the gRPC clients to communicate with the services.
"""
import argparse
import logging
import sys
import time

import grpc

# Add the current directory to the Python path
sys.path.append(".")

# Import the generated gRPC code
from auth.app.grpc import auth_pb2, auth_pb2_grpc
from user.app.grpc import user_pb2, user_pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("grpc_test")


def test_auth_service(host="localhost", port=50051):
    """Test the Auth service gRPC API."""
    logger.info(f"Testing Auth service at {host}:{port}")
    
    # Create a gRPC channel
    channel = grpc.insecure_channel(f"{host}:{port}")
    
    # Create a stub (client)
    stub = auth_pb2_grpc.AuthServiceStub(channel)
    
    try:
        # Test authentication
        logger.info("Testing authentication...")
        auth_request = auth_pb2.AuthRequest(
            email="admin@example.com",
            password="password123",
        )
        auth_response = stub.Authenticate(auth_request)
        logger.info(f"Authentication response: {auth_response}")
        
        # Test token validation
        logger.info("Testing token validation...")
        token_request = auth_pb2.TokenRequest(
            token=auth_response.access_token,
        )
        token_response = stub.ValidateToken(token_request)
        logger.info(f"Token validation response: {token_response}")
        
        # Test get user
        if token_response.is_valid:
            logger.info(f"Testing get user for ID: {token_response.user_id}")
            user_request = auth_pb2.UserRequest(
                user_id=token_response.user_id,
            )
            user_response = stub.GetUser(user_request)
            logger.info(f"User response: {user_response}")
        
        logger.info("Auth service tests completed successfully")
        return True
    
    except grpc.RpcError as e:
        logger.error(f"RPC error: {e.details()}")
        return False


def test_user_service(host="localhost", port=50052):
    """Test the User service gRPC API."""
    logger.info(f"Testing User service at {host}:{port}")
    
    # Create a gRPC channel
    channel = grpc.insecure_channel(f"{host}:{port}")
    
    # Create a stub (client)
    stub = user_pb2_grpc.UserServiceStub(channel)
    
    try:
        # Test get user profile
        logger.info("Testing get user profile...")
        profile_request = user_pb2.UserProfileRequest(
            user_id="test-user-id",
        )
        profile_response = stub.GetUserProfile(profile_request)
        logger.info(f"User profile response: {profile_response}")
        
        # Test get user preferences
        logger.info("Testing get user preferences...")
        preferences_request = user_pb2.UserPreferencesRequest(
            user_id="test-user-id",
        )
        preferences_response = stub.GetUserPreferences(preferences_request)
        logger.info(f"User preferences response: {preferences_response}")
        
        # Test get user activity
        logger.info("Testing get user activity...")
        activity_request = user_pb2.UserActivityRequest(
            user_id="test-user-id",
            limit=5,
            offset=0,
        )
        activity_response = stub.GetUserActivity(activity_request)
        logger.info(f"User activity response: {activity_response}")
        
        logger.info("User service tests completed successfully")
        return True
    
    except grpc.RpcError as e:
        logger.error(f"RPC error: {e.details()}")
        return False


def main():
    """Run the gRPC tests."""
    parser = argparse.ArgumentParser(description="Test gRPC communication between services")
    parser.add_argument("--auth-host", default="localhost", help="Auth service host")
    parser.add_argument("--auth-port", type=int, default=50051, help="Auth service port")
    parser.add_argument("--user-host", default="localhost", help="User service host")
    parser.add_argument("--user-port", type=int, default=50052, help="User service port")
    args = parser.parse_args()
    
    # Test Auth service
    auth_success = test_auth_service(args.auth_host, args.auth_port)
    
    # Test User service
    user_success = test_user_service(args.user_host, args.user_port)
    
    # Print summary
    logger.info("=== Test Summary ===")
    logger.info(f"Auth service: {'SUCCESS' if auth_success else 'FAILED'}")
    logger.info(f"User service: {'SUCCESS' if user_success else 'FAILED'}")
    
    # Exit with appropriate status code
    sys.exit(0 if auth_success and user_success else 1)


if __name__ == "__main__":
    main()