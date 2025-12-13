"""Upload File"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UploadFileFilesTool(BaseTool):
    """Upload File"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "upload_file_files",
            "description": "Upload File",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "process": {
                        "type": "boolean",
                        "description": "",
                        "default": True
                    },
                    "internal": {
                        "type": "boolean",
                        "description": "",
                        "default": False
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute upload_file_files operation."""
        self._log_execution_start(arguments)


        # Query parameter: process
        process = arguments.get("process", True)
        # Query parameter: internal
        internal = arguments.get("internal", False)

        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/files/", json_data=json_data)

        self._log_execution_end(response)
        return response