"""Archive All Chats"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ArchiveAllChatsChatsArchiveAllTool(BaseTool):
    """Archive All Chats"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "archive_all_chats_chats_archive_all",
            "description": "Archive All Chats",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute archive_all_chats_chats_archive_all operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/chats/archive/all", json_data=json_data)

        self._log_execution_end(response)
        return response