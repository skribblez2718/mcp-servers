"""Reindex Knowledge Files"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ReindexKnowledgeFilesKnowledgeReindexTool(BaseTool):
    """Reindex Knowledge Files"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "reindex_knowledge_files_knowledge_reindex",
            "description": "Reindex Knowledge Files",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute reindex_knowledge_files_knowledge_reindex operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/knowledge/reindex", json_data=json_data)

        self._log_execution_end(response)
        return response