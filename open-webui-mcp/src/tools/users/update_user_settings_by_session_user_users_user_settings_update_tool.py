"""Update User Settings By Session User"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateUserSettingsBySessionUserUsersUserSettingsUpdateTool(BaseTool):
    """Update User Settings By Session User"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_user_settings_by_session_user_users_user_settings_update",
            "description": "Update User Settings By Session User",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_user_settings_by_session_user_users_user_settings_update operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/users/user/settings/update", json_data=json_data)

        self._log_execution_end(response)
        return response