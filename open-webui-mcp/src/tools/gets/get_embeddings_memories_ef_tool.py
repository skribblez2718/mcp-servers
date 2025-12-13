"""Get Embeddings"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetEmbeddingsMemoriesEfTool(BaseTool):
    """Get Embeddings"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_embeddings_memories_ef",
            "description": "Get Embeddings",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_embeddings_memories_ef operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/memories/ef", params=params)

        self._log_execution_end(response)
        return response