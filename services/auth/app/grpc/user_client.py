"""gRPC client for communicating with the User service."""
import logging
import time
from typing import Dict, List, Optional

import grpc

from app.core.config import settings
from app.grpc import user_pb2, user_pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("user_grpc_client")


class UserServiceClient:
    """Client for the User service gRPC API."""

    def __init__(self, address: Optional[str] = None):
        """Initialize the client with the User service address."""
        self.address = address or f"{settings.USER_SERVICE_HOST}:{settings.USER_SERVICE_PORT}"
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
        """Connect to the User service."""
        if self.channel is None:
            logger.info(f"Connecting to User service at {self.address}")
            self.channel = grpc.insecure_channel(
                self.address, 
                options=self._channel_options
            )
            self.stub = user_pb2_grpc.UserServiceStub(self.channel)

    def close(self):
        """Close the connection to the User service."""
        if self.channel is not None:
            logger.info("Closing connection to User service")
            self.channel.close()
            self.channel = None
            self.stub = None

    def get_user_profile(self, user_id: str) -> Optional[user_pb2.UserProfileResponse]:
        """Get user profile by ID."""
        self.connect()
        try:
            logger.info(f"Getting user profile: {user_id}")
            request = user_pb2.UserProfileRequest(user_id=user_id)
            response = self.stub.GetUserProfile(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Get user profile failed: {e.details()}")
            return None

    def update_user_profile(
        self,
        user_id: str,
        display_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        bio: Optional[str] = None,
        location: Optional[str] = None,
        website: Optional[str] = None,
    ) -> Optional[user_pb2.UserProfileResponse]:
        """Update user profile."""
        self.connect()
        try:
            logger.info(f"Updating user profile: {user_id}")
            request = user_pb2.UpdateUserProfileRequest(user_id=user_id)
            
            # Set fields that are provided
            if display_name is not None:
                request.display_name = display_name
            if avatar_url is not None:
                request.avatar_url = avatar_url
            if bio is not None:
                request.bio = bio
            if location is not None:
                request.location = location
            if website is not None:
                request.website = website
            
            response = self.stub.UpdateUserProfile(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Update user profile failed: {e.details()}")
            return None

    def get_user_preferences(self, user_id: str) -> Optional[user_pb2.UserPreferencesResponse]:
        """Get user preferences."""
        self.connect()
        try:
            logger.info(f"Getting user preferences: {user_id}")
            request = user_pb2.UserPreferencesRequest(user_id=user_id)
            response = self.stub.GetUserPreferences(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Get user preferences failed: {e.details()}")
            return None

    def update_user_preferences(
        self,
        user_id: str,
        theme: Optional[str] = None,
        language: Optional[str] = None,
        notifications_enabled: Optional[bool] = None,
        notification_channels: Optional[List[str]] = None,
        additional_preferences: Optional[Dict[str, str]] = None,
    ) -> Optional[user_pb2.UserPreferencesResponse]:
        """Update user preferences."""
        self.connect()
        try:
            logger.info(f"Updating user preferences: {user_id}")
            request = user_pb2.UpdateUserPreferencesRequest(user_id=user_id)
            
            # Set fields that are provided
            if theme is not None:
                request.theme = theme
            if language is not None:
                request.language = language
            if notifications_enabled is not None:
                request.notifications_enabled = notifications_enabled
            if notification_channels is not None:
                request.notification_channels.extend(notification_channels)
            if additional_preferences is not None:
                request.additional_preferences.update(additional_preferences)
            
            response = self.stub.UpdateUserPreferences(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Update user preferences failed: {e.details()}")
            return None

    def get_user_activity(
        self, user_id: str, limit: int = 10, offset: int = 0
    ) -> Optional[user_pb2.UserActivityResponse]:
        """Get user activity."""
        self.connect()
        try:
            logger.info(f"Getting user activity: {user_id}")
            request = user_pb2.UserActivityRequest(
                user_id=user_id,
                limit=limit,
                offset=offset,
            )
            response = self.stub.GetUserActivity(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Get user activity failed: {e.details()}")
            return None

    def record_user_activity(
        self,
        user_id: str,
        activity_type: str,
        description: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Optional[user_pb2.RecordUserActivityResponse]:
        """Record user activity."""
        self.connect()
        try:
            logger.info(f"Recording user activity: {user_id} - {activity_type}")
            request = user_pb2.RecordUserActivityRequest(
                user_id=user_id,
                activity_type=activity_type,
                description=description,
            )
            
            if metadata is not None:
                request.metadata.update(metadata)
            
            response = self.stub.RecordUserActivity(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Record user activity failed: {e.details()}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[user_pb2.UserProfileResponse]:
        """Get user by email."""
        self.connect()
        try:
            logger.info(f"Getting user by email: {email}")
            request = user_pb2.UserEmailRequest(email=email)
            response = self.stub.GetUserByEmail(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Get user by email failed: {e.details()}")
            return None
    
    def search_users(
        self, query: str, limit: int = 10, offset: int = 0, filters: Optional[List[str]] = None
    ) -> Optional[user_pb2.SearchUsersResponse]:
        """Search users."""
        self.connect()
        try:
            logger.info(f"Searching users with query: {query}")
            request = user_pb2.SearchUsersRequest(
                query=query,
                limit=limit,
                offset=offset,
            )
            
            if filters is not None:
                request.filters.extend(filters)
            
            response = self.stub.SearchUsers(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Search users failed: {e.details()}")
            return None
    
    def health_check(self, service: str = "auth") -> Optional[user_pb2.HealthCheckResponse]:
        """Health check endpoint."""
        self.connect()
        try:
            logger.info(f"Health check for User service from: {service}")
            request = user_pb2.HealthCheckRequest(service=service)
            response = self.stub.HealthCheck(request)
            return response
        except grpc.RpcError as e:
            logger.error(f"Health check failed: {e.details()}")
            return None
    
    def with_deadline(self, timeout_seconds: float = 5.0):
        """Create a new client with a deadline."""
        client = UserServiceClient(self.address)
        client.connect()
        client.stub = client.stub.with_call_credentials(
            lambda context, callback: callback(
                [('deadline', str(time.time() + timeout_seconds))], None
            )
        )
        return client