"""Update Folder Name By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateFolderNameByIdFoldersIdUpdateTool(BaseTool):
    """Update Folder Name By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_folder_name_by_id_folders_id_update",
            "description": "Update Folder Name By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The folder ID to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "The new name for the folder"
                    },
                    "data": {
                        "type": "object",
                        "description": "Optional additional data for the folder",
                        "additionalProperties": True
                    }
                },
                "required": ["id", "name"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_folder_name_by_id_folders_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request with FolderForm schema
        json_data = {
            "name": arguments.get("name")
        }
        if arguments.get("data"):
            json_data["data"] = arguments.get("data")

        response = await self.client.post(f"/api/v1/folders/{id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response