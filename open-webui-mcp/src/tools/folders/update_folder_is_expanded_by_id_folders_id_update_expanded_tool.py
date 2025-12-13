"""Update Folder Is Expanded By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateFolderIsExpandedByIdFoldersIdUpdateExpandedTool(BaseTool):
    """Update Folder Is Expanded By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_folder_is_expanded_by_id_folders_id_update_expanded",
            "description": "Update Folder Is Expanded By Id",
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
        """Execute update_folder_is_expanded_by_id_folders_id_update_expanded operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/folders/{id}/update/expanded", json_data=json_data)

        self._log_execution_end(response)
        return response