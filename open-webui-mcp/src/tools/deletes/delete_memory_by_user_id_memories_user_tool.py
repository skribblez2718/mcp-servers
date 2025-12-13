"""Delete Memory By User Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteMemoryByUserIdMemoriesUserTool(BaseTool):
    """Delete Memory By User Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_memory_by_user_id_memories_user",
            "description": "Delete Memory By User Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_memory_by_user_id_memories_user operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.delete("/api/v1/memories/delete/user", params=params)

        self._log_execution_end(response)
        return response