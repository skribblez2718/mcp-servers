"""Create Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateModelOllamaCreateTool(BaseTool):
    """Create Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_model_ollama_create",
            "description": "Create Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "integer",
                        "description": "",
                        "default": 0
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_model_ollama_create operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        url_idx = arguments.get("url_idx", 0)

        # Build request
        json_data = {}

        response = await self.client.post("/ollama/api/create", json_data=json_data)

        self._log_execution_end(response)
        return response