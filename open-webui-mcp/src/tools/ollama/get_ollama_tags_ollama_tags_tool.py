"""Get Ollama Tags"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetOllamaTagsOllamaTagsTool(BaseTool):
    """Get Ollama Tags"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_ollama_tags_ollama_tags",
            "description": "Get Ollama Tags",
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
        """Execute get_ollama_tags_ollama_tags operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request
        params = {}
        if url_idx is not None:
            params["url_idx"] = url_idx

        response = await self.client.get("/ollama/api/tags", params=params)

        self._log_execution_end(response)
        return response