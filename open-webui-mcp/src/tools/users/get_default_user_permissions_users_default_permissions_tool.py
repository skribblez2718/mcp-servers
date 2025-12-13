"""Get Default User Permissions"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetDefaultUserPermissionsUsersDefaultPermissionsTool(BaseTool):
    """Get Default User Permissions"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_default_user_permissions_users_default_permissions",
            "description": "Get Default User Permissions",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_default_user_permissions_users_default_permissions operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/users/default/permissions", params=params)

        self._log_execution_end(response)
        return response