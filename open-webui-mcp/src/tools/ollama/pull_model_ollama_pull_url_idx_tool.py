"""Pull Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class PullModelOllamaPullUrlIdxTool(BaseTool):
    """Pull Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "pull_model_ollama_pull_url_idx",
            "description": "Pull Model from specific Ollama instance",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {"type": "integer", "description": "URL index"},
                    "model": {"type": ["string", "null"], "description": "Model name to pull"}
                },
                "required": ["url_idx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute pull_model_ollama_pull_url_idx operation."""
        self._log_execution_start(arguments)

        # Path parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request - ModelNameForm has additionalProperties
        json_data = {}
        if arguments.get("model") is not None:
            json_data["model"] = arguments["model"]
        for k, v in arguments.items():
            if k not in ["model", "url_idx"] and v is not None:
                json_data[k] = v

        response = await self.client.post(f"/ollama/api/pull/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response