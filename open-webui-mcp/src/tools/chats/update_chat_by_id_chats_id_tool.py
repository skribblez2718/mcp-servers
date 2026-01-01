"""Update Chat By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateChatByIdChatsIdTool(BaseTool):
    """Update Chat By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_chat_by_id_chats_id",
            "description": "Update Chat By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Chat ID"
                    },
                    "chat": {
                        "type": "object",
                        "additionalProperties": True,
                        "description": "Chat data object"
                    },
                    "folder_id": {
                        "type": ["string", "null"],
                        "description": "Optional folder ID to place the chat in"
                    }
                },
                "required": ["id", "chat"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_chat_by_id_chats_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request
        json_data = {"chat": arguments["chat"]}
        if arguments.get("folder_id") is not None:
            json_data["folder_id"] = arguments["folder_id"]

        response = await self.client.post(f"/api/v1/chats/{id}", json_data=json_data)

        self._log_execution_end(response)
        return response