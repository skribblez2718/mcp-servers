"""Get Embeddings"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


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
                        "description": ""
                    }
                },
                "required": ["text"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_embeddings_retrieval_ef_text operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: text
        text = arguments.get("text")
        if text:
            text = ToolInputValidator.validate_id(text, "text")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/retrieval/ef/{text}", params=params)

        self._log_execution_end(response)
        return response