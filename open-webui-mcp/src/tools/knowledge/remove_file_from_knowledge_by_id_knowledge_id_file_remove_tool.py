"""Remove File From Knowledge By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class RemoveFileFromKnowledgeByIdKnowledgeIdFileRemoveTool(BaseTool):
    """Remove File From Knowledge By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "remove_file_from_knowledge_by_id_knowledge_id_file_remove",
            "description": "Remove File From Knowledge By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The knowledge base ID"
                    },
                    "file_id": {
                        "type": "string",
                        "description": "The file ID to remove from the knowledge base"
                    }
                },
                "required": ["id", "file_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute remove_file_from_knowledge_by_id_knowledge_id_file_remove operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request with KnowledgeFileIdForm
        json_data = {
            "file_id": arguments.get("file_id")
        }

        response = await self.client.post(f"/api/v1/knowledge/{id}/file/remove", json_data=json_data)

        self._log_execution_end(response)
        return response