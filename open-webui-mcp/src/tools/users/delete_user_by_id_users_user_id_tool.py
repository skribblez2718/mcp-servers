"""Delete User By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteUserByIdUsersUserIdTool(BaseTool):
    """Delete User By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_user_by_id_users_user_id",
            "description": "Delete User By Id",
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
        """Execute delete_user_by_id_users_user_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: user_id
        user_id = arguments.get("user_id")
        if user_id:
            user_id = ToolInputValidator.validate_id(user_id, "user_id")


        # Build request
        params = {}

        response = await self.client.delete(f"/api/v1/users/{user_id}", params=params)

        self._log_execution_end(response)
        return response