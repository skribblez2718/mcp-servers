"""Push Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class PushModelOllamaPushTool(BaseTool):
    """Push Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "push_model_ollama_push",
            "description": "Push Model to Ollama registry",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Model name to push"},
                    "insecure": {"type": ["boolean", "null"], "description": "Allow insecure connections"},
                    "stream": {"type": ["boolean", "null"], "description": "Stream the response"},
                    "url_idx": {"type": ["integer", "null"], "description": "URL index"}
                },
                "required": ["model"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute push_model_ollama_push operation."""
        self._log_execution_start(arguments)

        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request - PushModelForm
        json_data = {"model": arguments["model"]}
        if arguments.get("insecure") is not None:
            json_data["insecure"] = arguments["insecure"]
        if arguments.get("stream") is not None:
            json_data["stream"] = arguments["stream"]

        params = {}
        if url_idx is not None:
            params["url_idx"] = url_idx

        response = await self.client.delete("/ollama/api/push", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response