"""gRPC server implementation for the User service."""
import logging
import time
from concurrent import futures
from datetime import datetime, timezone
from typing import Dict, List, Optional

import grpc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.grpc import user_pb2, user_pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("user_grpc_server")


class UserServicer(user_pb2_grpc.UserServiceServicer):
    """Implementation of the UserService gRPC service."""

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

    def GetUserProfile(
        self, request: user_pb2.UserProfileRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserProfileResponse:
        """Get user profile by ID."""
        logger.info(f"Getting user profile: {request.user_id}")
        
        # In a real implementation, you would fetch the user profile from the database
        # For this example, we'll return a mock profile
        
        return user_pb2.UserProfileResponse(
            user_id=request.user_id,
            email=f"user{request.user_id}@example.com",
            full_name=f"User {request.user_id}",
            display_name=f"User_{request.user_id}",
            avatar_url=f"https://example.com/avatars/{request.user_id}.jpg",
            bio="This is a mock user profile",
            location="Somewhere",
            website="https://example.com",
            created_at=int(time.time()) - 86400,  # 1 day ago
            updated_at=int(time.time()),
        )

    def UpdateUserProfile(
        self, request: user_pb2.UpdateUserProfileRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserProfileResponse:
        """Update user profile."""
        logger.info(f"Updating user profile: {request.user_id}")
        
        # In a real implementation, you would update the user profile in the database
        # For this example, we'll return a mock updated profile
        
        return user_pb2.UserProfileResponse(
            user_id=request.user_id,
            email=f"user{request.user_id}@example.com",
            full_name=f"User {request.user_id}",
            display_name=request.display_name if request.HasField("display_name") else f"User_{request.user_id}",
            avatar_url=request.avatar_url if request.HasField("avatar_url") else f"https://example.com/avatars/{request.user_id}.jpg",
            bio=request.bio if request.HasField("bio") else "This is a mock user profile",
            location=request.location if request.HasField("location") else "Somewhere",
            website=request.website if request.HasField("website") else "https://example.com",
            created_at=int(time.time()) - 86400,  # 1 day ago
            updated_at=int(time.time()),
        )

    def GetUserPreferences(
        self, request: user_pb2.UserPreferencesRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserPreferencesResponse:
        """Get user preferences."""
        logger.info(f"Getting user preferences: {request.user_id}")
        
        # In a real implementation, you would fetch the user preferences from the database
        # For this example, we'll return mock preferences
        
        return user_pb2.UserPreferencesResponse(
            user_id=request.user_id,
            theme="dark",
            language="en",
            notifications_enabled=True,
            notification_channels=["email", "push"],
            additional_preferences={"sidebar": "expanded", "font_size": "medium"},
        )

    def UpdateUserPreferences(
        self, request: user_pb2.UpdateUserPreferencesRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserPreferencesResponse:
        """Update user preferences."""
        logger.info(f"Updating user preferences: {request.user_id}")
        
        # In a real implementation, you would update the user preferences in the database
        # For this example, we'll return mock updated preferences
        
        return user_pb2.UserPreferencesResponse(
            user_id=request.user_id,
            theme=request.theme if request.HasField("theme") else "dark",
            language=request.language if request.HasField("language") else "en",
            notifications_enabled=request.notifications_enabled if request.HasField("notifications_enabled") else True,
            notification_channels=request.notification_channels or ["email", "push"],
            additional_preferences=request.additional_preferences or {"sidebar": "expanded", "font_size": "medium"},
        )

    def GetUserActivity(
        self, request: user_pb2.UserActivityRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserActivityResponse:
        """Get user activity."""
        logger.info(f"Getting user activity: {request.user_id}")
        
        # In a real implementation, you would fetch the user activity from the database
        # For this example, we'll return mock activities
        
        activities = []
        for i in range(1, 6):  # 5 mock activities
            activities.append(
                user_pb2.Activity(
                    id=f"activity_{i}",
                    user_id=request.user_id,
                    activity_type=f"type_{i % 3 + 1}",
                    description=f"Activity {i} description",
                    metadata={"key1": f"value{i}", "key2": f"value{i+1}"},
                    created_at=int(time.time()) - (i * 3600),  # i hours ago
                )
            )
        
        return user_pb2.UserActivityResponse(
            user_id=request.user_id,
            activities=activities,
            total_count=len(activities),
        )

    def RecordUserActivity(
        self, request: user_pb2.RecordUserActivityRequest, context: grpc.ServicerContext
    ) -> user_pb2.RecordUserActivityResponse:
        """Record user activity."""
        logger.info(f"Recording user activity: {request.user_id} - {request.activity_type}")
        
        # In a real implementation, you would record the activity in the database
        # For this example, we'll return a mock response
        
        return user_pb2.RecordUserActivityResponse(
            activity_id=f"activity_{int(time.time())}",
            success=True,
        )
    
    def GetUserByEmail(
        self, request: user_pb2.UserEmailRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserProfileResponse:
        """Get user by email."""
        logger.info(f"Getting user by email: {request.email}")
        
        # In a real implementation, you would fetch the user from the database by email
        # For this example, we'll return a mock user
        
        # Extract a user ID from the email for demonstration purposes
        user_id = request.email.split("@")[0].replace("user", "")
        
        return user_pb2.UserProfileResponse(
            user_id=user_id,
            email=request.email,
            full_name=f"User {user_id}",
            display_name=f"User_{user_id}",
            avatar_url=f"https://example.com/avatars/{user_id}.jpg",
            bio="This is a mock user profile",
            location="Somewhere",
            website="https://example.com",
            created_at=int(time.time()) - 86400,  # 1 day ago
            updated_at=int(time.time()),
        )
    
    def SearchUsers(
        self, request: user_pb2.SearchUsersRequest, context: grpc.ServicerContext
    ) -> user_pb2.SearchUsersResponse:
        """Search users."""
        logger.info(f"Searching users with query: {request.query}")
        
        # In a real implementation, you would search users in the database
        # For this example, we'll return mock users
        
        users = []
        for i in range(1, 6):  # 5 mock users
            users.append(
                user_pb2.UserProfileResponse(
                    user_id=f"user{i}",
                    email=f"user{i}@example.com",
                    full_name=f"User {i}",
                    display_name=f"User_{i}",
                    avatar_url=f"https://example.com/avatars/{i}.jpg",
                    bio=f"This is user {i}'s profile",
                    location="Somewhere",
                    website="https://example.com",
                    created_at=int(time.time()) - 86400,  # 1 day ago
                    updated_at=int(time.time()),
                )
            )
        
        return user_pb2.SearchUsersResponse(
            users=users,
            total_count=len(users),
        )
    
    def HealthCheck(
        self, request: user_pb2.HealthCheckRequest, context: grpc.ServicerContext
    ) -> user_pb2.HealthCheckResponse:
        """Health check endpoint."""
        logger.info(f"Health check from: {request.service}")
        
        # In a real implementation, you might check database connectivity, etc.
        return user_pb2.HealthCheckResponse(
            status=True,
            message="User service is healthy",
            timestamp=int(time.time())
        )


def serve(port: int = 50052):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"User gRPC server started on port {port}")
    return server