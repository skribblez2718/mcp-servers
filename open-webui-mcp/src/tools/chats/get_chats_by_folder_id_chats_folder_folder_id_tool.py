"""Get Chats By Folder Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetChatsByFolderIdChatsFolderFolderIdTool(BaseTool):
    """Get Chats By Folder Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_chats_by_folder_id_chats_folder_folder_id",
            "description": "Get Chats By Folder Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "folder_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["folder_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_chats_by_folder_id_chats_folder_folder_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: folder_id
        folder_id = arguments.get("folder_id")
        if folder_id:
            folder_id = ToolInputValidator.validate_id(folder_id, "folder_id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/chats/folder/{folder_id}", params=params)

        self._log_execution_end(response)
        return response