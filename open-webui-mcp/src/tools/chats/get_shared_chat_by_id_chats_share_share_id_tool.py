"""Get Shared Chat By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetSharedChatByIdChatsShareShareIdTool(BaseTool):
    """Get Shared Chat By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_shared_chat_by_id_chats_share_share_id",
            "description": "Get Shared Chat By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "share_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["share_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_shared_chat_by_id_chats_share_share_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: share_id
        share_id = arguments.get("share_id")
        if share_id:
            share_id = ToolInputValidator.validate_id(share_id, "share_id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/chats/share/{share_id}", params=params)

        self._log_execution_end(response)
        return response