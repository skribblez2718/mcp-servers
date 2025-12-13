"""Update Rag Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateRagConfigRetrievalConfigUpdateTool(BaseTool):
    """Update Rag Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_rag_config_retrieval_config_update",
            "description": "Update Rag Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_rag_config_retrieval_config_update operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/retrieval/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response