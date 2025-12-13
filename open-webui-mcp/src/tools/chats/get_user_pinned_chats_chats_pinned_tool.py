"""Get User Pinned Chats"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserPinnedChatsChatsPinnedTool(BaseTool):
    """Get User Pinned Chats"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_pinned_chats_chats_pinned",
            "description": "Get User Pinned Chats",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_pinned_chats_chats_pinned operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/chats/pinned", params=params)

        self._log_execution_end(response)
        return response