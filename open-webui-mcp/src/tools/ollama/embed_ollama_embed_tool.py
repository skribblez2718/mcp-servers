"""Embed"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class EmbedOllamaEmbedTool(BaseTool):
    """Embed"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "embed_ollama_embed",
            "description": "Embed",
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
        """Execute embed_ollama_embed operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request
        json_data = {}

        response = await self.client.post("/ollama/api/embed", json_data=json_data)

        self._log_execution_end(response)
        return response