"""Get Embedding Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetEmbeddingConfigRetrievalEmbeddingTool(BaseTool):
    """Get Embedding Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_embedding_config_retrieval_embedding",
            "description": "Get Embedding Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_embedding_config_retrieval_embedding operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/retrieval/embedding", params=params)

        self._log_execution_end(response)
        return response