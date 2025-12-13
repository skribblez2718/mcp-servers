"""Get User Settings By Session User"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserSettingsBySessionUserUsersUserSettingsTool(BaseTool):
    """Get User Settings By Session User"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_settings_by_session_user_users_user_settings",
            "description": "Get User Settings By Session User",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_settings_by_session_user_users_user_settings operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/users/user/settings", params=params)

        self._log_execution_end(response)
        return response