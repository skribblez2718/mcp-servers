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
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute import_chat_chats_import operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/chats/import", json_data=json_data)

        self._log_execution_end(response)
        return response