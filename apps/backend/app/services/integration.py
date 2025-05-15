import httpx
from typing import Dict, Any, Optional

from app.schemas.integration import ConnectorExecuteRequest, ConnectorExecuteResponse


class DataIntegrationService:
    async def execute_connector(self, request: ConnectorExecuteRequest) -> ConnectorExecuteResponse:
        """Execute a connector action"""
        if request.connector_type == "REST_API_CALL":
            return await self._execute_rest_api_call(request)
        elif request.connector_type == "SLACK_NOTIFICATION":
            return await self._execute_slack_notification(request)
        else:
            return ConnectorExecuteResponse(
                status="failed",
                error=f"Unsupported connector type: {request.connector_type}"
            )
    
    async def _execute_rest_api_call(self, request: ConnectorExecuteRequest) -> ConnectorExecuteResponse:
        """Execute a REST API call"""
        try:
            # Validate request
            if not request.config.url:
                return ConnectorExecuteResponse(
                    status="failed",
                    error="URL is required for REST API calls"
                )
            
            # Only GET is supported in MVP
            if request.config.method and request.config.method.upper() != "GET":
                return ConnectorExecuteResponse(
                    status="failed",
                    error=f"Unsupported HTTP method: {request.config.method}. Only GET is supported in MVP."
                )
            
            # Make the request
            async with httpx.AsyncClient() as client:
                headers = request.config.headers or {}
                response = await client.get(request.config.url, headers=headers)
                
                # Parse the response
                try:
                    response_data = response.json()
                except:
                    response_data = {"text": response.text}
                
                return ConnectorExecuteResponse(
                    status="success" if response.status_code < 400 else "failed",
                    response=response_data,
                    error=f"HTTP error: {response.status_code}" if response.status_code >= 400 else None
                )
        except Exception as e:
            return ConnectorExecuteResponse(
                status="failed",
                error=f"Error executing REST API call: {str(e)}"
            )
    
    async def _execute_slack_notification(self, request: ConnectorExecuteRequest) -> ConnectorExecuteResponse:
        """Execute a Slack notification"""
        # For MVP, we'll just simulate sending a Slack message
        # In a real implementation, this would use the Slack API
        
        try:
            # Validate request
            if not request.config.url:
                return ConnectorExecuteResponse(
                    status="failed",
                    error="Webhook URL is required for Slack notifications"
                )
            
            if not request.payload or "text" not in request.payload:
                return ConnectorExecuteResponse(
                    status="failed",
                    error="Payload with 'text' field is required for Slack notifications"
                )
            
            # Simulate sending a message
            # In a real implementation, we would make an API call to Slack
            
            return ConnectorExecuteResponse(
                status="success",
                response={
                    "message": "Slack notification sent successfully",
                    "channel": request.payload.get("channel", "general"),
                    "text": request.payload.get("text"),
                }
            )
        except Exception as e:
            return ConnectorExecuteResponse(
                status="failed",
                error=f"Error sending Slack notification: {str(e)}"
            )


data_integration_service = DataIntegrationService()
