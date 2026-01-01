"""Delete Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteModelOllamaTool(BaseTool):
    """Delete Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_model_ollama",
            "description": "Delete Model from Ollama",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": ["string", "null"], "description": "Model name to delete"},
                    "url_idx": {"type": ["integer", "null"], "description": "URL index"}
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_model_ollama operation."""
        self._log_execution_start(arguments)

        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request - ModelNameForm has additionalProperties
        json_data = {}
        if arguments.get("model") is not None:
            json_data["model"] = arguments["model"]
        for k, v in arguments.items():
            if k not in ["model", "url_idx"] and v is not None:
                json_data[k] = v

        params = {}
        if url_idx is not None:
            params["url_idx"] = url_idx

        response = await self.client.delete("/ollama/api/delete", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response