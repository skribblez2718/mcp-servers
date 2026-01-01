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
                    "content": {
                        "type": "string",
                        "description": "The query content to search memories"
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of results to return (default: 1)"
                    }
                },
                "required": ["content"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute query_memory_memories_query operation."""
        self._log_execution_start(arguments)

        # Build request body per QueryMemoryForm schema
        json_data = {
            "content": arguments.get("content")
        }
        # Add optional k parameter if provided
        if arguments.get("k") is not None:
            json_data["k"] = arguments.get("k")

        response = await self.client.post("/api/v1/memories/query", json_data=json_data)

        self._log_execution_end(response)
        return response