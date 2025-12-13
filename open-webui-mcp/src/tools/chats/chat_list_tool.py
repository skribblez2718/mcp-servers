"""Chat list tool - List all chats with pagination."""

from typing import Any
from src.tools.base import BaseTool
from src.models.chat import Chat
from src.models.base import PaginatedResponse
from src.utils.validation import ToolInputValidator


class ChatListTool(BaseTool):
    """List all chats with pagination support.

    Retrieves chats for the current user with optional filtering.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition with schema
        """
        return {
            "name": "chat_list",
            "description": "List all chats for the current user with pagination support",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of chats to return (1-1000)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset in the list of chats",
                        "default": 0,
                        "minimum": 0
                    },
                    "archived": {
                        "type": "boolean",
                        "description": "Filter archived chats only",
                        "default": False
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute chat list retrieval.

        Args:
            arguments: Tool arguments with limit, offset, archived

        Returns:
            Dict with chats list and pagination info

        Raises:
            ValidationError: If arguments invalid
            HTTPError: If API call fails
        """
        self._log_execution_start(arguments)

        # Extract and validate parameters
        limit = arguments.get("limit", 10)
        offset = arguments.get("offset", 0)
        archived = arguments.get("archived", False)

        limit, offset = ToolInputValidator.validate_pagination(limit, offset)

        # Build API request params
        params = {
            "limit": limit,
            "offset": offset,
        }

        if archived:
            params["archived"] = "true"

        # Call API
        response_data = await self.client.get("/api/v1/chats", params=params)

        # Transform response
        result = {
            "chats": response_data.get("data", response_data.get("chats", [])),
            "total": response_data.get("total", len(response_data.get("data", []))),
            "limit": limit,
            "offset": offset,
            "has_next": response_data.get("has_next", False)
        }

        self._log_execution_end(result)

        return result
