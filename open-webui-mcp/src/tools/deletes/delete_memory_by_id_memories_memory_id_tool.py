"""Delete Memory By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteMemoryByIdMemoriesMemoryIdTool(BaseTool):
    """Delete Memory By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_memory_by_id_memories_memory_id",
            "description": "Delete Memory By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["memory_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_memory_by_id_memories_memory_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: memory_id
        memory_id = arguments.get("memory_id")
        if memory_id:
            memory_id = ToolInputValidator.validate_id(memory_id, "memory_id")


        # Build request
        params = {}

        response = await self.client.delete(f"/api/v1/memories/{memory_id}", params=params)

        self._log_execution_end(response)
        return response