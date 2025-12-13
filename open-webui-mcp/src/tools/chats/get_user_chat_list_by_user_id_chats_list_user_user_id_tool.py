"""Get User Chat List By User Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserChatListByUserIdChatsListUserUserIdTool(BaseTool):
    """Get User Chat List By User Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_chat_list_by_user_id_chats_list_user_user_id",
            "description": "Get User Chat List By User Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": ""
                    },
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
                "required": ["user_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_chat_list_by_user_id_chats_list_user_user_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: user_id
        user_id = arguments.get("user_id")
        if user_id:
            user_id = ToolInputValidator.validate_id(user_id, "user_id")

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

        response = await self.client.get(f"/api/v1/chats/list/user/{user_id}", params=params)

        self._log_execution_end(response)
        return response