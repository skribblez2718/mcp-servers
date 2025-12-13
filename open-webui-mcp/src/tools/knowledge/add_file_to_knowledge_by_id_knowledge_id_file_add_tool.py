"""Add File To Knowledge By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class AddFileToKnowledgeByIdKnowledgeIdFileAddTool(BaseTool):
    """Add File To Knowledge By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "add_file_to_knowledge_by_id_knowledge_id_file_add",
            "description": "Add File To Knowledge By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute add_file_to_knowledge_by_id_knowledge_id_file_add operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/knowledge/{id}/file/add", json_data=json_data)

        self._log_execution_end(response)
        return response