"""gRPC client for communicating with the Auth service."""
import logging
import time
from typing import Dict, List, Optional

import grpc

from app.core.config import settings
from app.grpc import auth_pb2, auth_pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("auth_grpc_client")


class AuthServiceClient:
    """Client for the Auth service gRPC API."""

    def __init__(self, address: Optional[str] = None):
        """Initialize the client with the Auth service address."""
        self.address = address or settings.AUTH_SERVICE_ADDRESS
        self.channel = None
        self.stub = None
        self._channel_options = [
            ('grpc.keepalive_time_ms', 10000),  # Send keepalive ping every 10 seconds
            ('grpc.keepalive_timeout_ms', 5000),  # Keepalive ping timeout after 5 seconds
            ('grpc.keepalive_permit_without_calls', True),  # Allow keepalive pings when there are no calls
            ('grpc.http2.max_pings_without_data', 0),  # Allow unlimited pings without data
            ('grpc.http2.min_time_between_pings_ms', 10000),  # Minimum time between pings
            ('grpc.http2.min_ping_interval_without_data_ms', 5000),  # Minimum time between pings without data
            ('grpc.lb_policy_name', 'round_robin'),  # Use round-robin load balancing
        ]

    def __enter__(self):
        """Create a gRPC channel when entering a context."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the gRPC channel when exiting a context."""
        self.close()

    def connect(self):
        """Connect to the Auth service."""
        if self.channel is None:
            logger.info(f"Connecting to Auth service at {self.address}")
            self.channel = grpc.insecure_channel(
                self.address, 
                options=self._channel_options
            )
            self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def close(self):
        """Close the connection to the Auth service."""
        if self.channel is not None:
            logger.info("Closing connection to Auth service")
            self.channel.close()
            self.channel = None
            self.stub = None

    def authenticate(self, email: str, password: str) -> Optional[auth_pb2.AuthResponse]:
        """Authenticate a user with the Auth service."""
        self.connect()
        try:
            logger.info(f"Authenticating user: {email}")
            request = auth_pb2.AuthRequest(email=email, password=password)
            response = self.stub.Authenticate(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Authentication failed: {e.details()}")
            return None

    def validate_token(self, token: str) -> Optional[auth_pb2.TokenValidationResponse]:
        """Validate a token with the Auth service."""
        self.connect()
        try:
            logger.info("Validating token")
            request = auth_pb2.TokenRequest(token=token)
            response = self.stub.ValidateToken(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Token validation failed: {e.details()}")
            return None

    def refresh_token(self, refresh_token: str) -> Optional[auth_pb2.AuthResponse]:
        """Refresh an access token using a refresh token."""
        self.connect()
        try:
            logger.info("Refreshing token")
            request = auth_pb2.RefreshTokenRequest(refresh_token=refresh_token)
            response = self.stub.RefreshToken(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Token refresh failed: {e.details()}")
            return None

    def get_user(self, user_id: str) -> Optional[auth_pb2.UserResponse]:
        """Get user information by ID."""
        self.connect()
        try:
            logger.info(f"Getting user: {user_id}")
            request = auth_pb2.UserRequest(user_id=user_id)
            response = self.stub.GetUser(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Get user failed: {e.details()}")
            return None

    def create_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        is_active: bool = True,
        is_superuser: bool = False,
    ) -> Optional[auth_pb2.UserResponse]:
        """Create a new user."""
        self.connect()
        try:
            logger.info(f"Creating user: {email}")
            request = auth_pb2.CreateUserRequest(
                email=email,
                password=password,
                full_name=full_name or "",
                is_active=is_active,
                is_superuser=is_superuser,
            )
            response = self.stub.CreateUser(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Create user failed: {e.details()}")
            return None

    def update_user(
        self,
        user_id: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        full_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_superuser: Optional[bool] = None,
    ) -> Optional[auth_pb2.UserResponse]:
        """Update user information."""
        self.connect()
        try:
            logger.info(f"Updating user: {user_id}")
            request = auth_pb2.UpdateUserRequest(user_id=user_id)
            
            # Set fields that are provided
            if email is not None:
                request.email = email
            if password is not None:
                request.password = password
            if full_name is not None:
                request.full_name = full_name
            if is_active is not None:
                request.is_active = is_active
            if is_superuser is not None:
                request.is_superuser = is_superuser
            
            response = self.stub.UpdateUser(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Update user failed: {e.details()}")
            return None

    def delete_user(self, user_id: str) -> Optional[auth_pb2.DeleteUserResponse]:
        """Delete a user."""
        self.connect()
        try:
            logger.info(f"Deleting user: {user_id}")
            request = auth_pb2.UserRequest(user_id=user_id)
            response = self.stub.DeleteUser(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Delete user failed: {e.details()}")
            return None
    
    def check_email_exists(self, email: str) -> Optional[auth_pb2.EmailExistsResponse]:
        """Check if an email exists."""
        self.connect()
        try:
            logger.info(f"Checking if email exists: {email}")
            request = auth_pb2.EmailRequest(email=email)
            response = self.stub.CheckEmailExists(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Check email failed: {e.details()}")
            return None
    
    def get_user_roles(self, user_id: str) -> Optional[auth_pb2.UserRolesResponse]:
        """Get user roles."""
        self.connect()
        try:
            logger.info(f"Getting roles for user: {user_id}")
            request = auth_pb2.UserRequest(user_id=user_id)
            response = self.stub.GetUserRoles(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Get user roles failed: {e.details()}")
            return None
    
    def health_check(self, service: str = "user") -> Optional[auth_pb2.HealthCheckResponse]:
        """Health check endpoint."""
        self.connect()
        try:
            logger.info(f"Health check for Auth service from: {service}")
            request = auth_pb2.HealthCheckRequest(service=service)
            response = self.stub.HealthCheck(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Health check failed: {e.details()}")
            return None
    
    def with_deadline(self, timeout_seconds: float = 5.0):
        """Create a new client with a deadline."""
        client = AuthServiceClient(self.address)
        client.connect()
        client.stub = client.stub.with_call_credentials(
            lambda context, callback: callback(
                [('deadline', str(time.time() + timeout_seconds))], None
            )
        )
        return client