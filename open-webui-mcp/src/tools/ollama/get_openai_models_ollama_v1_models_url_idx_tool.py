"""Get Openai Models"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetOpenaiModelsOllamaV1ModelsUrlIdxTool(BaseTool):
    """Get Openai Models"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_openai_models_ollama_v1_models_url_idx",
            "description": "Get Openai Models",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["url_idx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_openai_models_ollama_v1_models_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request
        params = {}

        response = await self.client.get(f"/ollama/v1/models/{url_idx}", params=params)

        self._log_execution_end(response)
        return response