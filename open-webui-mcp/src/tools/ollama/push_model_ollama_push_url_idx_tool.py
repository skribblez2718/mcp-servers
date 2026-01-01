"""Push Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class PushModelOllamaPushUrlIdxTool(BaseTool):
    """Push Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "push_model_ollama_push_url_idx",
            "description": "Push Model to specific Ollama instance",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {"type": ["integer", "null"], "description": "URL index"},
                    "model": {"type": "string", "description": "Model name to push"},
                    "insecure": {"type": ["boolean", "null"], "description": "Allow insecure connections"},
                    "stream": {"type": ["boolean", "null"], "description": "Stream the response"}
                },
                "required": ["url_idx", "model"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute push_model_ollama_push_url_idx operation."""
        self._log_execution_start(arguments)

        # Path parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request - PushModelForm
        json_data = {"model": arguments["model"]}
        if arguments.get("insecure") is not None:
            json_data["insecure"] = arguments["insecure"]
        if arguments.get("stream") is not None:
            json_data["stream"] = arguments["stream"]

        response = await self.client.delete(f"/ollama/api/push/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response