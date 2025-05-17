"""
OAuth 2.0 configuration for grimOS API
"""
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from typing import Dict, List, Optional, Any

from app.core.config import settings

# OAuth configuration
config = Config()
oauth = OAuth(config)

# Google OAuth
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account'
    }
)

# GitHub OAuth
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Microsoft OAuth
oauth.register(
    name='microsoft',
    client_id=settings.MICROSOFT_CLIENT_ID,
    client_secret=settings.MICROSOFT_CLIENT_SECRET,
    server_metadata_url='https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# List of available OAuth providers
OAUTH_PROVIDERS = ['google', 'github', 'microsoft']

async def get_oauth_user_info(provider: str, token: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get user information from the OAuth provider based on the access token.
    
    Args:
        provider: The OAuth provider name
        token: The OAuth token information
        
    Returns:
        Dictionary containing standardized user information
    """
    client = oauth.create_client(provider)
    
    if provider == 'google':
        resp = await client.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
        profile = resp.json()
        return {
            'email': profile.get('email'),
            'name': profile.get('name'),
            'picture': profile.get('picture'),
            'provider': 'google',
            'provider_id': profile.get('sub')
        }
    
    elif provider == 'github':
        resp = await client.get('user', token=token)
        profile = resp.json()
        
        # GitHub doesn't always return email in profile, get it separately
        email_resp = await client.get('user/emails', token=token)
        emails = email_resp.json()
        primary_email = next((email['email'] for email in emails if email['primary']), None)
        
        return {
            'email': primary_email,
            'name': profile.get('name'),
            'picture': profile.get('avatar_url'),
            'provider': 'github',
            'provider_id': str(profile.get('id'))
        }
    
    elif provider == 'microsoft':
        resp = await client.get('https://graph.microsoft.com/v1.0/me', token=token)
        profile = resp.json()
        return {
            'email': profile.get('mail') or profile.get('userPrincipalName'),
            'name': profile.get('displayName'),
            'picture': None,  # Microsoft Graph API doesn't directly provide a profile picture URL
            'provider': 'microsoft',
            'provider_id': profile.get('id')
        }
    
    raise ValueError(f"Unsupported OAuth provider: {provider}")
