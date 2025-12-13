"""Update File Data Content By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateFileDataContentByIdFilesIdDataContentUpdateTool(BaseTool):
    """Update File Data Content By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_file_data_content_by_id_files_id_data_content_update",
            "description": "Update File Data Content By Id",
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
        """Execute update_file_data_content_by_id_files_id_data_content_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/files/{id}/data/content/update", json_data=json_data)

        self._log_execution_end(response)
        return response