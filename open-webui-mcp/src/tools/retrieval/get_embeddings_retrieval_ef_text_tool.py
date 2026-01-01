"""Get Embeddings"""

from typing import Any
from urllib.parse import quote
from src.tools.base import BaseTool


class GetEmbeddingsRetrievalEfTextTool(BaseTool):
    """Get Embeddings"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_embeddings_retrieval_ef_text",
            "description": "Get Embeddings",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to get embeddings for"
                    }
                },
                "required": ["text"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_embeddings_retrieval_ef_text operation."""
        self._log_execution_start(arguments)

        # Get text parameter and URL-encode it for path usage
        text = arguments.get("text", "")
        encoded_text = quote(text, safe="")

        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/retrieval/ef/{encoded_text}", params=params)

        self._log_execution_end(response)
        return response