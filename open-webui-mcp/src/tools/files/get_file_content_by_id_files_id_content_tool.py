"""Get File Content By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetFileContentByIdFilesIdContentTool(BaseTool):
    """Get File Content By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_file_content_by_id_files_id_content",
            "description": "Get File Content By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    },
                    "attachment": {
                        "type": "boolean",
                        "description": "",
                        "default": False
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_file_content_by_id_files_id_content operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Query parameter: attachment
        attachment = arguments.get("attachment", False)

        # Build request
        params = {}
        if attachment is not None:
            params["attachment"] = attachment

        response = await self.client.get(f"/api/v1/files/{id}/content", params=params)

        self._log_execution_end(response)
        return response