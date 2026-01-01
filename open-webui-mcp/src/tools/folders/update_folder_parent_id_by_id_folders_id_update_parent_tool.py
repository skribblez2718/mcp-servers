"""Update Folder Parent Id By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateFolderParentIdByIdFoldersIdUpdateParentTool(BaseTool):
    """Update Folder Parent Id By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_folder_parent_id_by_id_folders_id_update_parent",
            "description": "Update Folder Parent Id By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The folder ID to update"
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "The new parent folder ID (null for root level)"
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_folder_parent_id_by_id_folders_id_update_parent operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request with FolderParentIdForm schema
        json_data = {}
        if "parent_id" in arguments:
            json_data["parent_id"] = arguments.get("parent_id")

        response = await self.client.post(f"/api/v1/folders/{id}/update/parent", json_data=json_data)

        self._log_execution_end(response)
        return response