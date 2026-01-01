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
            "description": "Unload Model from Ollama memory",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": ["string", "null"], "description": "Model name to unload"}
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute unload_model_ollama_unload operation."""
        self._log_execution_start(arguments)

        # Build request - ModelNameForm has additionalProperties
        json_data = {}
        if arguments.get("model") is not None:
            json_data["model"] = arguments["model"]
        # Pass through any additional properties
        for k, v in arguments.items():
            if k not in ["model"] and v is not None:
                json_data[k] = v

        response = await self.client.post("/ollama/api/unload", json_data=json_data)

        self._log_execution_end(response)
        return response