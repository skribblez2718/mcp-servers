"""Unload Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UnloadModelOllamaUnloadTool(BaseTool):
    """Unload Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "unload_model_ollama_unload",
            "description": "Unload Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute unload_model_ollama_unload operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/ollama/api/unload", json_data=json_data)

        self._log_execution_end(response)
        return response