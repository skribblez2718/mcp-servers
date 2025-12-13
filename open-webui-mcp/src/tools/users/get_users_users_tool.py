"""Get Users"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUsersUsersTool(BaseTool):
    """Get Users"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_users_users",
            "description": "Get Users",
            "inputSchema": {
                "type": "object",
                "properties": {
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
                    },
                    "page": {
                        "type": "string",
                        "description": "",
                        "default": 1
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_users_users operation."""
        self._log_execution_start(arguments)


        # Query parameter: query
        query = arguments.get("query")
        # Query parameter: order_by
        order_by = arguments.get("order_by")
        # Query parameter: direction
        direction = arguments.get("direction")
        # Query parameter: page
        page = arguments.get("page", 1)

        # Build request
        params = {}
        if query is not None:
            params["query"] = query
        if order_by is not None:
            params["order_by"] = order_by
        if direction is not None:
            params["direction"] = direction
        if page is not None:
            params["page"] = page

        response = await self.client.get("/api/v1/users/", params=params)

        self._log_execution_end(response)
        return response