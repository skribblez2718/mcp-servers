"""Serve Cache File"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ServeCacheFileCachePathTool(BaseTool):
    """Serve Cache File"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "serve_cache_file_cache_path",
            "description": "Serve Cache File",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["path"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute serve_cache_file_cache_path operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: path
        path = arguments.get("path")
        if path:
            path = ToolInputValidator.validate_id(path, "path")


        # Build request
        params = {}

        response = await self.client.get(f"/cache/{path}", params=params)

        self._log_execution_end(response)
        return response