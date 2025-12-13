"""Get User Info By Session User"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserInfoBySessionUserUsersUserInfoTool(BaseTool):
    """Get User Info By Session User"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_info_by_session_user_users_user_info",
            "description": "Get User Info By Session User",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_info_by_session_user_users_user_info operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/users/user/info", params=params)

        self._log_execution_end(response)
        return response