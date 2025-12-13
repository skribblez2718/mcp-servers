"""Query Memory"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class QueryMemoryMemoriesQueryTool(BaseTool):
    """Query Memory"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "query_memory_memories_query",
            "description": "Query Memory",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute query_memory_memories_query operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/memories/query", json_data=json_data)

        self._log_execution_end(response)
        return response