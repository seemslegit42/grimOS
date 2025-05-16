"""
Slack Connector for the Interoperability Engine
"""
import httpx
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class SlackMessage(BaseModel):
    """Model for a Slack message"""
    channel: str = Field(..., description="Channel to send the message to")
    text: str = Field(..., description="Text content of the message")
    blocks: Optional[List[Dict[str, Any]]] = Field(None, description="Blocks for rich message formatting")
    thread_ts: Optional[str] = Field(None, description="Thread timestamp to reply to")
    mrkdwn: Optional[bool] = Field(True, description="Whether to parse the message as markdown")
    unfurl_links: Optional[bool] = Field(True, description="Whether to unfurl links")
    unfurl_media: Optional[bool] = Field(True, description="Whether to unfurl media")

class SlackConnector:
    """Connector for Slack API"""
    
    def __init__(self, api_token: str, base_url: str = "https://slack.com/api"):
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Slack API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/auth.test",
                    headers=self.headers
                )
                
                data = response.json()
                if not data.get("ok", False):
                    return {
                        "success": False,
                        "message": f"Failed to connect to Slack: {data.get('error', 'Unknown error')}"
                    }
                
                return {
                    "success": True,
                    "message": f"Successfully connected to Slack as {data.get('user')} in team {data.get('team')}",
                    "details": data
                }
        
        except Exception as e:
            logger.exception(f"Error testing Slack connection: {str(e)}")
            return {
                "success": False,
                "message": f"Error connecting to Slack: {str(e)}"
            }
    
    async def send_message(self, message: SlackMessage) -> Dict[str, Any]:
        """Send a message to a Slack channel"""
        try:
            async with httpx.AsyncClient() as client:
                payload = message.dict(exclude_none=True)
                
                response = await client.post(
                    f"{self.base_url}/chat.postMessage",
                    headers=self.headers,
                    json=payload
                )
                
                data = response.json()
                if not data.get("ok", False):
                    logger.error(f"Failed to send Slack message: {data.get('error', 'Unknown error')}")
                    return {
                        "success": False,
                        "message": f"Failed to send message: {data.get('error', 'Unknown error')}"
                    }
                
                return {
                    "success": True,
                    "message": "Message sent successfully",
                    "details": {
                        "ts": data.get("ts"),
                        "channel": data.get("channel")
                    }
                }
        
        except Exception as e:
            logger.exception(f"Error sending Slack message: {str(e)}")
            return {
                "success": False,
                "message": f"Error sending message: {str(e)}"
            }
    
    async def get_channels(self) -> Dict[str, Any]:
        """Get a list of channels in the workspace"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/conversations.list",
                    headers=self.headers,
                    params={"types": "public_channel,private_channel"}
                )
                
                data = response.json()
                if not data.get("ok", False):
                    return {
                        "success": False,
                        "message": f"Failed to get channels: {data.get('error', 'Unknown error')}"
                    }
                
                channels = data.get("channels", [])
                return {
                    "success": True,
                    "message": f"Retrieved {len(channels)} channels",
                    "channels": [
                        {
                            "id": channel.get("id"),
                            "name": channel.get("name"),
                            "is_private": channel.get("is_private", False),
                            "num_members": channel.get("num_members", 0)
                        }
                        for channel in channels
                    ]
                }
        
        except Exception as e:
            logger.exception(f"Error getting Slack channels: {str(e)}")
            return {
                "success": False,
                "message": f"Error getting channels: {str(e)}"
            }
    
    async def get_users(self) -> Dict[str, Any]:
        """Get a list of users in the workspace"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/users.list",
                    headers=self.headers
                )
                
                data = response.json()
                if not data.get("ok", False):
                    return {
                        "success": False,
                        "message": f"Failed to get users: {data.get('error', 'Unknown error')}"
                    }
                
                users = data.get("members", [])
                return {
                    "success": True,
                    "message": f"Retrieved {len(users)} users",
                    "users": [
                        {
                            "id": user.get("id"),
                            "name": user.get("name"),
                            "real_name": user.get("real_name"),
                            "is_bot": user.get("is_bot", False),
                            "is_admin": user.get("is_admin", False)
                        }
                        for user in users
                        if not user.get("deleted", False)
                    ]
                }
        
        except Exception as e:
            logger.exception(f"Error getting Slack users: {str(e)}")
            return {
                "success": False,
                "message": f"Error getting users: {str(e)}"
            }
    
    @classmethod
    def get_operations(cls) -> List[Dict[str, Any]]:
        """Get the list of operations supported by this connector"""
        return [
            {
                "id": "send_message",
                "name": "Send Message",
                "description": "Send a message to a Slack channel",
                "parameters": {
                    "channel": {
                        "type": "string",
                        "description": "Channel ID or name to send the message to",
                        "required": True
                    },
                    "text": {
                        "type": "string",
                        "description": "Text content of the message",
                        "required": True
                    },
                    "blocks": {
                        "type": "array",
                        "description": "Blocks for rich message formatting",
                        "required": False
                    },
                    "thread_ts": {
                        "type": "string",
                        "description": "Thread timestamp to reply to",
                        "required": False
                    }
                },
                "returns": {
                    "success": {
                        "type": "boolean",
                        "description": "Whether the operation was successful"
                    },
                    "message": {
                        "type": "string",
                        "description": "Status message"
                    },
                    "details": {
                        "type": "object",
                        "description": "Additional details about the operation"
                    }
                }
            },
            {
                "id": "get_channels",
                "name": "Get Channels",
                "description": "Get a list of channels in the workspace",
                "parameters": {},
                "returns": {
                    "success": {
                        "type": "boolean",
                        "description": "Whether the operation was successful"
                    },
                    "message": {
                        "type": "string",
                        "description": "Status message"
                    },
                    "channels": {
                        "type": "array",
                        "description": "List of channels"
                    }
                }
            },
            {
                "id": "get_users",
                "name": "Get Users",
                "description": "Get a list of users in the workspace",
                "parameters": {},
                "returns": {
                    "success": {
                        "type": "boolean",
                        "description": "Whether the operation was successful"
                    },
                    "message": {
                        "type": "string",
                        "description": "Status message"
                    },
                    "users": {
                        "type": "array",
                        "description": "List of users"
                    }
                }
            }
        ]
    
    @classmethod
    def get_auth_config(cls) -> Dict[str, Any]:
        """Get the authentication configuration for this connector"""
        return {
            "type": "api_key",
            "fields": [
                {
                    "name": "api_token",
                    "label": "API Token",
                    "description": "Slack Bot User OAuth Token",
                    "required": True,
                    "secret": True
                }
            ]
        }
    
    @classmethod
    def get_connector_info(cls) -> Dict[str, Any]:
        """Get information about this connector"""
        return {
            "name": "Slack",
            "description": "Connect to Slack to send messages and interact with channels",
            "icon": "slack",
            "category": "Communication",
            "auth_type": "api_key",
            "operations": cls.get_operations(),
            "auth_config": cls.get_auth_config()
        }