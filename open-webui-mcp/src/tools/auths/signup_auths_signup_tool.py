"""Signup"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SignupAuthsSignupTool(BaseTool):
    """Signup"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "signup_auths_signup",
            "description": "Signup",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "User display name"
                    },
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    },
                    "password": {
                        "type": "string",
                        "description": "User password"
                    },
                    "profile_image_url": {
                        "type": ["string", "null"],
                        "description": "URL to user's profile image",
                        "default": "/user.png"
                    }
                },
                "required": ["name", "email", "password"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute signup_auths_signup operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "name": arguments.get("name"),
            "email": arguments.get("email"),
            "password": arguments.get("password")
        }
        # Add optional fields if provided
        if arguments.get("profile_image_url") is not None:
            json_data["profile_image_url"] = arguments.get("profile_image_url")

        response = await self.client.post("/api/v1/auths/signup", json_data=json_data)

        self._log_execution_end(response)
        return response