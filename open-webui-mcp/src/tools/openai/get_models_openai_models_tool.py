"""Get Models"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetModelsOpenaiModelsTool(BaseTool):
    """Get Models"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_models_openai_models",
            "description": "Get Models",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_models_openai_models operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request
        params = {}
        if url_idx is not None:
            params["url_idx"] = url_idx

        response = await self.client.get("/openai/models", params=params)

        self._log_execution_end(response)
        return response