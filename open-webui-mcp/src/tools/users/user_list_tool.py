"""User list tool - List all users."""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UserListTool(BaseTool):
    """List all users with pagination.

    Requires admin permissions in production.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition with schema
        """
        return {
            "name": "user_list",
            "description": "List all users (admin permission required)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of users to return",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset in the list",
                        "default": 0,
                        "minimum": 0
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute user list retrieval.

        Args:
            arguments: Tool arguments

        Returns:
            Dict with users list

        Raises:
            ValidationError: If arguments invalid
            AuthError: If insufficient permissions
            HTTPError: If API call fails
        """
        self._log_execution_start(arguments)

        limit = arguments.get("limit", 50)
        offset = arguments.get("offset", 0)

        limit, offset = ToolInputValidator.validate_pagination(limit, offset)

        params = {"limit": limit, "offset": offset}
        response_data = await self.client.get("/api/v1/users/", params=params)

        result = {
            "users": response_data.get("data", response_data.get("users", [])),
            "total": response_data.get("total", len(response_data.get("data", []))),
            "limit": limit,
            "offset": offset
        }

        self._log_execution_end(result)

        return result
