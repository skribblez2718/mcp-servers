"""Embeddings"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class EmbeddingsEmbeddingsTool(BaseTool):
    """OpenAI-compatible embeddings endpoint.  This handler:   - Performs user/model checks and dispatches to the correct backend.   - Supports OpenAI, Ollama, arena models, pipelines, and any compatible provider.  Args:     request (Request): Request context.   """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "embeddings_embeddings",
            "description": "OpenAI-compatible embeddings endpoint.  This handler:   - Performs user/model checks and dispatches to the correct backend.   - Supports OpenAI, Ollama, arena models, pipelines, and any compatible provider.  Args:     request (Request): Request context.   ",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute embeddings_embeddings operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/embeddings", json_data=json_data)

        self._log_execution_end(response)
        return response