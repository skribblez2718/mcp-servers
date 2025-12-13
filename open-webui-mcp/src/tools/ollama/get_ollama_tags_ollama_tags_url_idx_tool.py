"""Get Ollama Tags"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetOllamaTagsOllamaTagsUrlIdxTool(BaseTool):
    """Get Ollama Tags"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_ollama_tags_ollama_tags_url_idx",
            "description": "Get Ollama Tags",
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
        """Execute get_ollama_tags_ollama_tags_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request
        params = {}

        response = await self.client.get(f"/ollama/api/tags/{url_idx}", params=params)

        self._log_execution_end(response)
        return response