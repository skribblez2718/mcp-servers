"""Get Archived Session User Chat List"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetArchivedSessionUserChatListChatsArchivedTool(BaseTool):
    """Get Archived Session User Chat List"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_archived_session_user_chat_list_chats_archived",
            "description": "Get Archived Session User Chat List",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "string",
                        "description": ""
                    },
                    "query": {
                        "type": "string",
                        "description": ""
                    },
                    "order_by": {
                        "type": "string",
                        "description": ""
                    },
                    "direction": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_archived_session_user_chat_list_chats_archived operation."""
        self._log_execution_start(arguments)


        # Query parameter: page
        page = arguments.get("page")
        # Query parameter: query
        query = arguments.get("query")
        # Query parameter: order_by
        order_by = arguments.get("order_by")
        # Query parameter: direction
        direction = arguments.get("direction")

        # Build request
        params = {}
        if page is not None:
            params["page"] = page
        if query is not None:
            params["query"] = query
        if order_by is not None:
            params["order_by"] = order_by
        if direction is not None:
            params["direction"] = direction

        response = await self.client.get("/api/v1/chats/archived", params=params)

        self._log_execution_end(response)
        return response