"""Import Chat"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ImportChatChatsImportTool(BaseTool):
    """Import Chat"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "import_chat_chats_import",
            "description": "Import Chat",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "chat": {
                        "type": "object",
                        "additionalProperties": True,
                        "description": "Chat data object to import"
                    },
                    "folder_id": {
                        "type": ["string", "null"],
                        "description": "Optional folder ID to place the chat in"
                    },
                    "meta": {
                        "type": ["object", "null"],
                        "additionalProperties": True,
                        "description": "Optional metadata object"
                    },
                    "pinned": {
                        "type": ["boolean", "null"],
                        "description": "Whether chat is pinned",
                        "default": False
                    },
                    "created_at": {
                        "type": ["integer", "null"],
                        "description": "Optional creation timestamp"
                    },
                    "updated_at": {
                        "type": ["integer", "null"],
                        "description": "Optional update timestamp"
                    }
                },
                "required": ["chat"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute import_chat_chats_import operation."""
        self._log_execution_start(arguments)

        # Build request - Note: API expects "chats" not "chat" despite OpenAPI spec
        json_data = {"chats": [arguments["chat"]]}
        if arguments.get("folder_id") is not None:
            json_data["folder_id"] = arguments["folder_id"]
        if arguments.get("meta") is not None:
            json_data["meta"] = arguments["meta"]
        if arguments.get("pinned") is not None:
            json_data["pinned"] = arguments["pinned"]
        if arguments.get("created_at") is not None:
            json_data["created_at"] = arguments["created_at"]
        if arguments.get("updated_at") is not None:
            json_data["updated_at"] = arguments["updated_at"]

        response = await self.client.post("/api/v1/chats/import", json_data=json_data)

        self._log_execution_end(response)
        return response