"""Get User Archived Chats"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserArchivedChatsChatsAllArchivedTool(BaseTool):
    """Get User Archived Chats"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_archived_chats_chats_all_archived",
            "description": "Get User Archived Chats",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_archived_chats_chats_all_archived operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/chats/all/archived", params=params)

        self._log_execution_end(response)
        return response