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
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to upload"
                    },
                    "process": {
                        "type": "boolean",
                        "description": "Whether to process the file after upload",
                        "default": True
                    },
                    "internal": {
                        "type": "boolean",
                        "description": "Whether this is an internal file",
                        "default": False
                    }
                },
                "required": ["file_path"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute upload_file_files operation."""
        self._log_execution_start(arguments)

        file_path = arguments["file_path"]

        # Query parameter: process
        process = arguments.get("process", True)
        # Query parameter: internal
        internal = arguments.get("internal", False)

        # Build query params
        params = {}
        if process is not None:
            params["process"] = process
        if internal is not None:
            params["internal"] = internal

        # Build request - file upload uses multipart/form-data
        response = await self.client.post_with_file(
            "/api/v1/files/",
            file_path=file_path,
            params=params
        )

        self._log_execution_end(response)
        return response