"""Update Admin Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateAdminConfigAuthsAdminConfigTool(BaseTool):
    """Update Admin Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_admin_config_auths_admin_config",
            "description": "Update Admin Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "SHOW_ADMIN_DETAILS": {
                        "type": "boolean",
                        "description": "Show admin details to users"
                    },
                    "WEBUI_URL": {
                        "type": "string",
                        "description": "WebUI base URL"
                    },
                    "ENABLE_SIGNUP": {
                        "type": "boolean",
                        "description": "Allow user signup"
                    },
                    "ENABLE_API_KEY": {
                        "type": "boolean",
                        "description": "Enable API key authentication"
                    },
                    "ENABLE_API_KEY_ENDPOINT_RESTRICTIONS": {
                        "type": "boolean",
                        "description": "Enable API key endpoint restrictions"
                    },
                    "API_KEY_ALLOWED_ENDPOINTS": {
                        "type": "string",
                        "description": "Allowed API endpoints for API keys"
                    },
                    "DEFAULT_USER_ROLE": {
                        "type": "string",
                        "description": "Default role for new users"
                    },
                    "JWT_EXPIRES_IN": {
                        "type": "string",
                        "description": "JWT token expiration time"
                    },
                    "ENABLE_COMMUNITY_SHARING": {
                        "type": "boolean",
                        "description": "Enable community sharing features"
                    },
                    "ENABLE_MESSAGE_RATING": {
                        "type": "boolean",
                        "description": "Enable message rating"
                    },
                    "ENABLE_CHANNELS": {
                        "type": "boolean",
                        "description": "Enable channels feature"
                    },
                    "ENABLE_NOTES": {
                        "type": "boolean",
                        "description": "Enable notes feature"
                    },
                    "ENABLE_USER_WEBHOOKS": {
                        "type": "boolean",
                        "description": "Enable user webhooks"
                    },
                    "PENDING_USER_OVERLAY_TITLE": {
                        "type": ["string", "null"],
                        "description": "Title for pending user overlay"
                    },
                    "PENDING_USER_OVERLAY_CONTENT": {
                        "type": ["string", "null"],
                        "description": "Content for pending user overlay"
                    },
                    "RESPONSE_WATERMARK": {
                        "type": ["string", "null"],
                        "description": "Watermark for responses"
                    }
                },
                "required": [
                    "SHOW_ADMIN_DETAILS", "WEBUI_URL", "ENABLE_SIGNUP", "ENABLE_API_KEY",
                    "ENABLE_API_KEY_ENDPOINT_RESTRICTIONS", "API_KEY_ALLOWED_ENDPOINTS",
                    "DEFAULT_USER_ROLE", "JWT_EXPIRES_IN", "ENABLE_COMMUNITY_SHARING",
                    "ENABLE_MESSAGE_RATING", "ENABLE_CHANNELS", "ENABLE_NOTES", "ENABLE_USER_WEBHOOKS"
                ]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_admin_config_auths_admin_config operation."""
        self._log_execution_start(arguments)



        # Build request - required fields
        json_data = {
            "SHOW_ADMIN_DETAILS": arguments.get("SHOW_ADMIN_DETAILS"),
            "WEBUI_URL": arguments.get("WEBUI_URL"),
            "ENABLE_SIGNUP": arguments.get("ENABLE_SIGNUP"),
            "ENABLE_API_KEY": arguments.get("ENABLE_API_KEY"),
            "ENABLE_API_KEY_ENDPOINT_RESTRICTIONS": arguments.get("ENABLE_API_KEY_ENDPOINT_RESTRICTIONS"),
            "API_KEY_ALLOWED_ENDPOINTS": arguments.get("API_KEY_ALLOWED_ENDPOINTS"),
            "DEFAULT_USER_ROLE": arguments.get("DEFAULT_USER_ROLE"),
            "JWT_EXPIRES_IN": arguments.get("JWT_EXPIRES_IN"),
            "ENABLE_COMMUNITY_SHARING": arguments.get("ENABLE_COMMUNITY_SHARING"),
            "ENABLE_MESSAGE_RATING": arguments.get("ENABLE_MESSAGE_RATING"),
            "ENABLE_CHANNELS": arguments.get("ENABLE_CHANNELS"),
            "ENABLE_NOTES": arguments.get("ENABLE_NOTES"),
            "ENABLE_USER_WEBHOOKS": arguments.get("ENABLE_USER_WEBHOOKS")
        }
        # Add optional fields if provided
        if arguments.get("PENDING_USER_OVERLAY_TITLE") is not None:
            json_data["PENDING_USER_OVERLAY_TITLE"] = arguments.get("PENDING_USER_OVERLAY_TITLE")
        if arguments.get("PENDING_USER_OVERLAY_CONTENT") is not None:
            json_data["PENDING_USER_OVERLAY_CONTENT"] = arguments.get("PENDING_USER_OVERLAY_CONTENT")
        if arguments.get("RESPONSE_WATERMARK") is not None:
            json_data["RESPONSE_WATERMARK"] = arguments.get("RESPONSE_WATERMARK")

        response = await self.client.post("/api/v1/auths/admin/config", json_data=json_data)

        self._log_execution_end(response)
        return response