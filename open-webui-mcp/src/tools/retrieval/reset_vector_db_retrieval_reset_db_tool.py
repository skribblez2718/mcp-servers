"""Reset Vector Db"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ResetVectorDbRetrievalResetDbTool(BaseTool):
    """Reset Vector Db"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "reset_vector_db_retrieval_reset_db",
            "description": "Reset Vector Db",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute reset_vector_db_retrieval_reset_db operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/retrieval/reset/db", json_data=json_data)

        self._log_execution_end(response)
        return response