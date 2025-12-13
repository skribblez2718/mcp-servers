"""Get User Chat List By Tag Name"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserChatListByTagNameChatsTagsTool(BaseTool):
    """Get User Chat List By Tag Name"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_chat_list_by_tag_name_chats_tags",
            "description": "Get User Chat List By Tag Name",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_chat_list_by_tag_name_chats_tags operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/chats/tags", json_data=json_data)

        self._log_execution_end(response)
        return response