"""Copy Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CopyModelOllamaCopyTool(BaseTool):
    """Copy Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "copy_model_ollama_copy",
            "description": "Copy Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute copy_model_ollama_copy operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request
        json_data = {}

        response = await self.client.post("/ollama/api/copy", json_data=json_data)

        self._log_execution_end(response)
        return response