"""Get User Permissisions"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserPermissisionsUsersPermissionsTool(BaseTool):
    """Get User Permissisions"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_permissisions_users_permissions",
            "description": "Get User Permissisions",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_permissisions_users_permissions operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/users/permissions", params=params)

        self._log_execution_end(response)
        return response