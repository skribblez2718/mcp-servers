"""Update Default User Permissions"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateDefaultUserPermissionsUsersDefaultPermissionsTool(BaseTool):
    """Update Default User Permissions"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_default_user_permissions_users_default_permissions",
            "description": "Update Default User Permissions",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_default_user_permissions_users_default_permissions operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/users/default/permissions", json_data=json_data)

        self._log_execution_end(response)
        return response