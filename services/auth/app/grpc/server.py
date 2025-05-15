"""gRPC server implementation for the Auth service."""
import logging
import time
from concurrent import futures
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import grpc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.user import (
    authenticate_user,
    create_refresh_token,
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    update_user,
)
from app.db.session import SessionLocal
from app.grpc import auth_pb2, auth_pb2_grpc
from app.schemas.auth import UserCreate, UserUpdate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("auth_grpc_server")


class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    """Implementation of the AuthService gRPC service."""

    def __init__(self):
        """Initialize the servicer."""
        self.db = SessionLocal

    def _get_db(self) -> Session:
        """Get a database session."""
        db = self.db()
        try:
            return db
        finally:
            db.close()

    def Authenticate(
        self, request: auth_pb2.AuthRequest, context: grpc.ServicerContext
    ) -> auth_pb2.AuthResponse:
        """Authenticate a user and return tokens."""
        logger.info(f"Authenticating user: {request.email}")
        
        db = self._get_db()
        user = authenticate_user(db, request.email, request.password)
        
        if not user:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid credentials")
            return auth_pb2.AuthResponse()
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.id),
            expires_delta=access_token_expires,
        )
        
        # Create refresh token
        refresh_token = f"refresh_{str(user.id)}_{int(time.time())}"
        
        # Store refresh token in database
        create_refresh_token(
            db=db,
            user_id=str(user.id),
            token=refresh_token,
            expires_in_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            user_agent="gRPC client",
            ip_address="internal",
        )
        
        return auth_pb2.AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def ValidateToken(
        self, request: auth_pb2.TokenRequest, context: grpc.ServicerContext
    ) -> auth_pb2.TokenValidationResponse:
        """Validate a token and return user information."""
        logger.info("Validating token")
        
        # This is a simplified implementation
        # In a real-world scenario, you would decode and verify the JWT token
        # For now, we'll assume the token is valid if it starts with "valid_"
        
        if request.token.startswith("valid_"):
            # Extract user_id from token (in a real implementation, you'd decode the JWT)
            user_id = request.token.split("_")[1]
            
            db = self._get_db()
            user = get_user(db, user_id)
            
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return auth_pb2.TokenValidationResponse()
            
            return auth_pb2.TokenValidationResponse(
                is_valid=True,
                user_id=str(user.id),
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                expires_at=int(time.time()) + 3600,  # 1 hour from now
            )
        else:
            return auth_pb2.TokenValidationResponse(
                is_valid=False,
            )

    def RefreshToken(
        self, request: auth_pb2.RefreshTokenRequest, context: grpc.ServicerContext
    ) -> auth_pb2.AuthResponse:
        """Refresh an access token using a refresh token."""
        logger.info("Refreshing token")
        
        # In a real implementation, you would validate the refresh token
        # For this example, we'll assume it's valid if it starts with "refresh_"
        
        if not request.refresh_token.startswith("refresh_"):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid refresh token")
            return auth_pb2.AuthResponse()
        
        # Extract user_id from token
        parts = request.refresh_token.split("_")
        if len(parts) < 3:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid refresh token format")
            return auth_pb2.AuthResponse()
        
        user_id = parts[1]
        
        db = self._get_db()
        user = get_user(db, user_id)
        
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return auth_pb2.AuthResponse()
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.id),
            expires_delta=access_token_expires,
        )
        
        # Create new refresh token
        new_refresh_token = f"refresh_{str(user.id)}_{int(time.time())}"
        
        # Store new refresh token in database
        create_refresh_token(
            db=db,
            user_id=str(user.id),
            token=new_refresh_token,
            expires_in_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            user_agent="gRPC client",
            ip_address="internal",
        )
        
        return auth_pb2.AuthResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def GetUser(
        self, request: auth_pb2.UserRequest, context: grpc.ServicerContext
    ) -> auth_pb2.UserResponse:
        """Get user information by ID."""
        logger.info(f"Getting user: {request.user_id}")
        
        db = self._get_db()
        user = get_user(db, request.user_id)
        
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return auth_pb2.UserResponse()
        
        return auth_pb2.UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name or "",
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=int(user.created_at.timestamp()),
            updated_at=int(user.updated_at.timestamp()),
        )

    def CreateUser(
        self, request: auth_pb2.CreateUserRequest, context: grpc.ServicerContext
    ) -> auth_pb2.UserResponse:
        """Create a new user."""
        logger.info(f"Creating user: {request.email}")
        
        db = self._get_db()
        
        # Check if email already exists
        existing_user = get_user_by_email(db, request.email)
        if existing_user:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Email already registered")
            return auth_pb2.UserResponse()
        
        # Create user
        user_in = UserCreate(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            is_active=request.is_active,
            is_superuser=request.is_superuser,
        )
        
        user = create_user(db, user_in)
        
        return auth_pb2.UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name or "",
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=int(user.created_at.timestamp()),
            updated_at=int(user.updated_at.timestamp()),
        )

    def UpdateUser(
        self, request: auth_pb2.UpdateUserRequest, context: grpc.ServicerContext
    ) -> auth_pb2.UserResponse:
        """Update user information."""
        logger.info(f"Updating user: {request.user_id}")
        
        db = self._get_db()
        user = get_user(db, request.user_id)
        
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return auth_pb2.UserResponse()
        
        # Create update object with only the fields that are set
        update_data = {}
        if request.HasField("email"):
            update_data["email"] = request.email
        if request.HasField("password"):
            update_data["password"] = request.password
        if request.HasField("full_name"):
            update_data["full_name"] = request.full_name
        if request.HasField("is_active"):
            update_data["is_active"] = request.is_active
        if request.HasField("is_superuser"):
            update_data["is_superuser"] = request.is_superuser
        
        user_in = UserUpdate(**update_data)
        updated_user = update_user(db, user, user_in)
        
        return auth_pb2.UserResponse(
            id=str(updated_user.id),
            email=updated_user.email,
            full_name=updated_user.full_name or "",
            is_active=updated_user.is_active,
            is_superuser=updated_user.is_superuser,
            created_at=int(updated_user.created_at.timestamp()),
            updated_at=int(updated_user.updated_at.timestamp()),
        )

    def DeleteUser(
        self, request: auth_pb2.UserRequest, context: grpc.ServicerContext
    ) -> auth_pb2.DeleteUserResponse:
        """Delete a user."""
        logger.info(f"Deleting user: {request.user_id}")
        
        db = self._get_db()
        user = get_user(db, request.user_id)
        
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return auth_pb2.DeleteUserResponse()
        
        delete_user(db, request.user_id)
        
        return auth_pb2.DeleteUserResponse(
            success=True,
            message=f"User {request.user_id} deleted successfully",
        )
    
    def CheckEmailExists(
        self, request: auth_pb2.EmailRequest, context: grpc.ServicerContext
    ) -> auth_pb2.EmailExistsResponse:
        """Check if an email exists."""
        logger.info(f"Checking if email exists: {request.email}")
        
        db = self._get_db()
        user = get_user_by_email(db, request.email)
        
        return auth_pb2.EmailExistsResponse(
            exists=user is not None
        )
    
    def GetUserRoles(
        self, request: auth_pb2.UserRequest, context: grpc.ServicerContext
    ) -> auth_pb2.UserRolesResponse:
        """Get user roles."""
        logger.info(f"Getting roles for user: {request.user_id}")
        
        db = self._get_db()
        user = get_user(db, request.user_id)
        
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return auth_pb2.UserRolesResponse()
        
        # In a real implementation, you would fetch the user's roles from the database
        # For this example, we'll return mock roles based on the user's superuser status
        roles = ["user"]
        permissions = {"read": "true"}
        
        if user.is_superuser:
            roles.append("admin")
            permissions["write"] = "true"
            permissions["delete"] = "true"
        
        return auth_pb2.UserRolesResponse(
            user_id=str(user.id),
            roles=roles,
            permissions=permissions
        )
    
    def HealthCheck(
        self, request: auth_pb2.HealthCheckRequest, context: grpc.ServicerContext
    ) -> auth_pb2.HealthCheckResponse:
        """Health check endpoint."""
        logger.info(f"Health check from: {request.service}")
        
        # In a real implementation, you might check database connectivity, etc.
        return auth_pb2.HealthCheckResponse(
            status=True,
            message="Auth service is healthy",
            timestamp=int(time.time())
        )


def serve(port: int = 50051):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"Auth gRPC server started on port {port}")
    return server