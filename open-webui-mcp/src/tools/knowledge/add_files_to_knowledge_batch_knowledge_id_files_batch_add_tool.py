"""Add Files To Knowledge Batch"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class AddFilesToKnowledgeBatchKnowledgeIdFilesBatchAddTool(BaseTool):
    """Add multiple files to a knowledge base"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "add_files_to_knowledge_batch_knowledge_id_files_batch_add",
            "description": "Add multiple files to a knowledge base",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The knowledge base ID"
                    },
                    "file_ids": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of file IDs to add to the knowledge base"
                    }
                },
                "required": ["id", "file_ids"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute add_files_to_knowledge_batch_knowledge_id_files_batch_add operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request - array of KnowledgeFileIdForm objects
        file_ids = arguments.get("file_ids", [])
        json_data = [{"file_id": fid} for fid in file_ids]

        response = await self.client.post(f"/api/v1/knowledge/{id}/files/batch/add", json_data=json_data)

        self._log_execution_end(response)
        return response