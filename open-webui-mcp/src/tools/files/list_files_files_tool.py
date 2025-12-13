"""List Files"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ListFilesFilesTool(BaseTool):
    """List Files"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "list_files_files",
            "description": "List Files",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "boolean",
                        "description": "",
                        "default": True
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute list_files_files operation."""
        self._log_execution_start(arguments)


        # Query parameter: content
        content = arguments.get("content", True)

        # Build request
        params = {}
        if content is not None:
            params["content"] = content

        response = await self.client.get("/api/v1/files/", params=params)

        self._log_execution_end(response)
        return response