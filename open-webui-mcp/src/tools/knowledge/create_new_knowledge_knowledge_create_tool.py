"""Create New Knowledge"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewKnowledgeKnowledgeCreateTool(BaseTool):
    """Create New Knowledge"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_knowledge_knowledge_create",
            "description": "Create New Knowledge",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_knowledge_knowledge_create operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/knowledge/create", json_data=json_data)

        self._log_execution_end(response)
        return response