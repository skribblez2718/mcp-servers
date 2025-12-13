"""Get Session User Chat List"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetSessionUserChatListChatsListTool(BaseTool):
    """Get Session User Chat List"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_session_user_chat_list_chats_list",
            "description": "Get Session User Chat List",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_session_user_chat_list_chats_list operation."""
        self._log_execution_start(arguments)


        # Query parameter: page
        page = arguments.get("page")

        # Build request
        params = {}
        if page is not None:
            params["page"] = page

        response = await self.client.get("/api/v1/chats/list", params=params)

        self._log_execution_end(response)
        return response