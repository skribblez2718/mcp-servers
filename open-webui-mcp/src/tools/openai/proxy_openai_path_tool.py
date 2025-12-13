"""Proxy"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ProxyOpenaiPathTool(BaseTool):
    """Deprecated: proxy all requests to OpenAI API"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "proxy_openai_path",
            "description": "Deprecated: proxy all requests to OpenAI API",
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
        """Execute proxy_openai_path operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: path
        path = arguments.get("path")
        if path:
            path = ToolInputValidator.validate_id(path, "path")


        # Build request
        json_data = {}

        response = await self.client.put(f"/openai/{path}", json_data=json_data)

        self._log_execution_end(response)
        return response