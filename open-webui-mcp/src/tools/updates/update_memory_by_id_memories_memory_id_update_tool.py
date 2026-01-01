"""Update Memory By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateMemoryByIdMemoriesMemoryIdUpdateTool(BaseTool):
    """Update Memory By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_memory_by_id_memories_memory_id_update",
            "description": "Update Memory By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "The ID of the memory to update"
                    },
                    "content": {
                        "type": "string",
                        "description": "The new content for the memory"
                    }
                },
                "required": ["memory_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_memory_by_id_memories_memory_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: memory_id
        memory_id = arguments.get("memory_id")
        if memory_id:
            memory_id = ToolInputValidator.validate_id(memory_id, "memory_id")

        # Build request body per MemoryUpdateModel schema
        json_data = {}
        if arguments.get("content") is not None:
            json_data["content"] = arguments.get("content")

        response = await self.client.post(f"/api/v1/memories/{memory_id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response