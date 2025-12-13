"""Search User Chats"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SearchUserChatsChatsSearchTool(BaseTool):
    """Search User Chats"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "search_user_chats_chats_search",
            "description": "Search User Chats",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": ""
                    },
                    "page": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["text"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute search_user_chats_chats_search operation."""
        self._log_execution_start(arguments)


        # Query parameter: text
        text = arguments.get("text")
        # Query parameter: page
        page = arguments.get("page")

        # Build request
        params = {}
        if text is not None:
            params["text"] = text
        if page is not None:
            params["page"] = page

        response = await self.client.get("/api/v1/chats/search", params=params)

        self._log_execution_end(response)
        return response