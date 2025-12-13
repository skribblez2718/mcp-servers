"""Reset Memory From Vector Db"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ResetMemoryFromVectorDbMemoriesResetTool(BaseTool):
    """Reset Memory From Vector Db"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "reset_memory_from_vector_db_memories_reset",
            "description": "Reset Memory From Vector Db",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute reset_memory_from_vector_db_memories_reset operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/memories/reset", json_data=json_data)

        self._log_execution_end(response)
        return response