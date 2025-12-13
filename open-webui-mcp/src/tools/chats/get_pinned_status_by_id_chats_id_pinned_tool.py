"""Get Pinned Status By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetPinnedStatusByIdChatsIdPinnedTool(BaseTool):
    """Get Pinned Status By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_pinned_status_by_id_chats_id_pinned",
            "description": "Get Pinned Status By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_pinned_status_by_id_chats_id_pinned operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/chats/{id}/pinned", params=params)

        self._log_execution_end(response)
        return response