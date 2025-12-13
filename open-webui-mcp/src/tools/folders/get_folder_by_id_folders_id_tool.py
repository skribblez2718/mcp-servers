"""Get Folder By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetFolderByIdFoldersIdTool(BaseTool):
    """Get Folder By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_folder_by_id_folders_id",
            "description": "Get Folder By Id",
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
        """Execute get_folder_by_id_folders_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/folders/{id}", params=params)

        self._log_execution_end(response)
        return response