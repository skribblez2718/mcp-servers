"""Create Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateModelOllamaCreateUrlIdxTool(BaseTool):
    """Create Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_model_ollama_create_url_idx",
            "description": "Create Model in specific Ollama instance",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {"type": "integer", "description": "URL index"},
                    "model": {"type": ["string", "null"], "description": "Model name"},
                    "stream": {"type": ["boolean", "null"], "description": "Stream the response"},
                    "path": {"type": ["string", "null"], "description": "Path to modelfile"}
                },
                "required": ["url_idx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_model_ollama_create_url_idx operation."""
        self._log_execution_start(arguments)

        # Path parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request - CreateModelForm has additionalProperties
        json_data = {}
        if arguments.get("model") is not None:
            json_data["model"] = arguments["model"]
        if arguments.get("stream") is not None:
            json_data["stream"] = arguments["stream"]
        if arguments.get("path") is not None:
            json_data["path"] = arguments["path"]
        for k, v in arguments.items():
            if k not in ["model", "stream", "path", "url_idx"] and v is not None:
                json_data[k] = v

        response = await self.client.post(f"/ollama/api/create/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response