"""Search Files"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SearchFilesFilesSearchTool(BaseTool):
    """Search for files by filename with support for wildcard patterns."""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "search_files_files_search",
            "description": "Search for files by filename with support for wildcard patterns.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename pattern to search for. Supports wildcards such as '*.txt'"
                    },
                    "content": {
                        "type": "boolean",
                        "description": "",
                        "default": True
                    }
                },
                "required": ["filename"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute search_files_files_search operation."""
        self._log_execution_start(arguments)


        # Query parameter: filename
        filename = arguments.get("filename")
        # Query parameter: content
        content = arguments.get("content", True)

        # Build request
        params = {}
        if filename is not None:
            params["filename"] = filename
        if content is not None:
            params["content"] = content

        response = await self.client.get("/api/v1/files/search", params=params)

        self._log_execution_end(response)
        return response