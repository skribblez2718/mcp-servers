"""Get All User Chats In Db"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetAllUserChatsInDbChatsAllDbTool(BaseTool):
    """Get All User Chats In Db"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_all_user_chats_in_db_chats_all_db",
            "description": "Get All User Chats In Db",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_all_user_chats_in_db_chats_all_db operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/chats/all/db", params=params)

        self._log_execution_end(response)
        return response