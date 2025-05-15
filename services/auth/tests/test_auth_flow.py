"""
Authentication Flow End-to-End Tests

These tests verify the complete authentication flow, including:
- User registration
- Login
- Token refresh
- Token validation
- Logout
"""

import os
import pytest
import requests
import time
from typing import Dict, Any, Tuple

# Test configuration
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:5000")
TEST_USER_EMAIL = "test_user@example.com"
TEST_USER_PASSWORD = "TestPassword123!"
TEST_USER_NAME = "Test User"


@pytest.fixture(scope="module")
def user_credentials() -> Dict[str, str]:
    """User credentials for testing"""
    return {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "full_name": TEST_USER_NAME,
    }


@pytest.fixture(scope="module")
def registered_user(user_credentials: Dict[str, str]) -> Dict[str, Any]:
    """Register a test user and return the created user data"""
    # Clean up any existing test user
    try:
        # Using direct auth service endpoint for cleanup
        response = requests.post(
            f"{AUTH_SERVICE_URL}/api/v1/users/find-by-email",
            json={"email": user_credentials["email"]},
            headers={"X-Service-Key": os.getenv("SERVICE_SECRET_KEY", "servicesecretkey")},
        )
        if response.status_code == 200:
            user_id = response.json().get("id")
            if user_id:
                requests.delete(
                    f"{AUTH_SERVICE_URL}/api/v1/users/{user_id}",
                    headers={"X-Service-Key": os.getenv("SERVICE_SECRET_KEY", "servicesecretkey")},
                )
    except Exception as e:
        print(f"Error during user cleanup: {e}")
    
    # Register new test user through API Gateway
    register_data = {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
        "full_name": user_credentials["full_name"],
    }
    
    response = requests.post(f"{API_GATEWAY_URL}/api/v1/auth/register", json=register_data)
    assert response.status_code == 201, f"Failed to register user: {response.text}"
    
    user_data = response.json()
    return user_data


@pytest.fixture(scope="module")
def auth_tokens(registered_user: Dict[str, Any], user_credentials: Dict[str, str]) -> Dict[str, str]:
    """Get authentication tokens by logging in"""
    login_data = {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
    }
    
    response = requests.post(f"{API_GATEWAY_URL}/api/v1/auth/login", json=login_data)
    assert response.status_code == 200, f"Failed to login: {response.text}"
    
    tokens = response.json()
    assert "access_token" in tokens, "No access token in response"
    assert "refresh_token" in tokens, "No refresh token in response"
    
    return tokens


def test_user_registration(user_credentials: Dict[str, str]):
    """Test user registration endpoint"""
    # Clean up any existing test user (same as in registered_user fixture)
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/api/v1/users/find-by-email",
            json={"email": user_credentials["email"]},
            headers={"X-Service-Key": os.getenv("SERVICE_SECRET_KEY", "servicesecretkey")},
        )
        if response.status_code == 200:
            user_id = response.json().get("id")
            if user_id:
                requests.delete(
                    f"{AUTH_SERVICE_URL}/api/v1/users/{user_id}",
                    headers={"X-Service-Key": os.getenv("SERVICE_SECRET_KEY", "servicesecretkey")},
                )
    except Exception as e:
        print(f"Error during user cleanup: {e}")
    
    # Register new user
    register_data = {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
        "full_name": user_credentials["full_name"],
    }
    
    response = requests.post(f"{API_GATEWAY_URL}/api/v1/auth/register", json=register_data)
    assert response.status_code == 201, f"Failed to register user: {response.text}"
    
    user_data = response.json()
    assert user_data["email"] == user_credentials["email"]
    assert "id" in user_data
    assert "is_active" in user_data
    assert user_data["is_active"] is True


def test_login(user_credentials: Dict[str, str]):
    """Test login endpoint"""
    login_data = {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
    }
    
    response = requests.post(f"{API_GATEWAY_URL}/api/v1/auth/login", json=login_data)
    assert response.status_code == 200, f"Failed to login: {response.text}"
    
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert "token_type" in tokens
    assert tokens["token_type"] == "bearer"


def test_access_protected_route(auth_tokens: Dict[str, str]):
    """Test accessing a protected route with the access token"""
    headers = {"Authorization": f"Bearer {auth_tokens['access_token']}"}
    
    response = requests.get(f"{API_GATEWAY_URL}/api/v1/users/me", headers=headers)
    assert response.status_code == 200, f"Failed to access protected route: {response.text}"
    
    user_data = response.json()
    assert user_data["email"] == TEST_USER_EMAIL


def test_token_refresh(auth_tokens: Dict[str, str]):
    """Test refreshing the access token"""
    refresh_data = {
        "refresh_token": auth_tokens["refresh_token"]
    }
    
    response = requests.post(f"{API_GATEWAY_URL}/api/v1/auth/refresh", json=refresh_data)
    assert response.status_code == 200, f"Failed to refresh token: {response.text}"
    
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    assert new_tokens["access_token"] != auth_tokens["access_token"]


def test_invalid_token():
    """Test using an invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    
    response = requests.get(f"{API_GATEWAY_URL}/api/v1/users/me", headers=headers)
    assert response.status_code == 401, f"Expected 401 for invalid token but got {response.status_code}"


def test_logout(auth_tokens: Dict[str, str]):
    """Test logout endpoint"""
    headers = {"Authorization": f"Bearer {auth_tokens['access_token']}"}
    
    response = requests.post(f"{API_GATEWAY_URL}/api/v1/auth/logout", headers=headers)
    assert response.status_code == 200, f"Failed to logout: {response.text}"
    
    # Verify token is invalidated
    response = requests.get(f"{API_GATEWAY_URL}/api/v1/users/me", headers=headers)
    assert response.status_code == 401, f"Token should be invalidated after logout"


def test_token_expiration():
    """Test token expiration (optional, only if we can manipulate token lifetime)"""
    # This test is optional as it requires a short token lifetime or the ability to modify it
    # For testing purposes, it might be better to have a specific endpoint that issues
    # short-lived tokens for testing
    pass
