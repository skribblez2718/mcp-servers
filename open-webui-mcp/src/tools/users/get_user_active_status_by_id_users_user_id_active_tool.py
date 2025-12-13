"""Get User Active Status By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserActiveStatusByIdUsersUserIdActiveTool(BaseTool):
    """Get User Active Status By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_active_status_by_id_users_user_id_active",
            "description": "Get User Active Status By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["user_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_active_status_by_id_users_user_id_active operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: user_id
        user_id = arguments.get("user_id")
        if user_id:
            user_id = ToolInputValidator.validate_id(user_id, "user_id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/users/{user_id}/active", params=params)

        self._log_execution_end(response)
        return response