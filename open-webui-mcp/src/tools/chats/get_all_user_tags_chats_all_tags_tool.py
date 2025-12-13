"""Get All User Tags"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetAllUserTagsChatsAllTagsTool(BaseTool):
    """Get All User Tags"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_all_user_tags_chats_all_tags",
            "description": "Get All User Tags",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_all_user_tags_chats_all_tags operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/chats/all/tags", params=params)

        self._log_execution_end(response)
        return response