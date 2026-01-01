"""Create New Chat"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewChatChatsNewTool(BaseTool):
    """Create New Chat"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_chat_chats_new",
            "description": "Create New Chat",
            "inputSchema": {
                "type": "object",
                "properties": {
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
                "required": ["chat"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_chat_chats_new operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {"chat": arguments["chat"]}
        if arguments.get("folder_id") is not None:
            json_data["folder_id"] = arguments["folder_id"]

        response = await self.client.post("/api/v1/chats/new", json_data=json_data)

        self._log_execution_end(response)
        return response