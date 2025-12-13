"""Get Ollama Loaded Models"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetOllamaLoadedModelsOllamaPsTool(BaseTool):
    """List models that are currently loaded into Ollama memory, and which node they are loaded on."""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_ollama_loaded_models_ollama_ps",
            "description": "List models that are currently loaded into Ollama memory, and which node they are loaded on.",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_ollama_loaded_models_ollama_ps operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/ollama/api/ps", params=params)

        self._log_execution_end(response)
        return response