"""Update User By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateUserByIdUsersUserIdUpdateTool(BaseTool):
    """Update User By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_user_by_id_users_user_id_update",
            "description": "Update User By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user ID to update (path parameter)"
                    },
                    "role": {
                        "type": "string",
                        "description": "User role (e.g., 'admin', 'user', 'pending')"
                    },
                    "name": {
                        "type": "string",
                        "description": "User display name"
                    },
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    },
                    "profile_image_url": {
                        "type": "string",
                        "description": "URL to user's profile image"
                    },
                    "password": {
                        "type": ["string", "null"],
                        "description": "New password (optional)"
                    }
                },
                "required": ["user_id", "role", "name", "email", "profile_image_url"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_user_by_id_users_user_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: user_id
        user_id = arguments.get("user_id")
        if user_id:
            user_id = ToolInputValidator.validate_id(user_id, "user_id")

        # Build request
        json_data = {
            "role": arguments.get("role"),
            "name": arguments.get("name"),
            "email": arguments.get("email"),
            "profile_image_url": arguments.get("profile_image_url")
        }
        if arguments.get("password") is not None:
            json_data["password"] = arguments.get("password")

        response = await self.client.post(f"/api/v1/users/{user_id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response