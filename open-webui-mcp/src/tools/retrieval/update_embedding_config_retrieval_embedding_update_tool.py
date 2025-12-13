"""Update Embedding Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateEmbeddingConfigRetrievalEmbeddingUpdateTool(BaseTool):
    """Update Embedding Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_embedding_config_retrieval_embedding_update",
            "description": "Update Embedding Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_embedding_config_retrieval_embedding_update operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/retrieval/embedding/update", json_data=json_data)

        self._log_execution_end(response)
        return response