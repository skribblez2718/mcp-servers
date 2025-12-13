"""Delete Entries From Collection"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteEntriesFromCollectionRetrievalTool(BaseTool):
    """Delete Entries From Collection"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_entries_from_collection_retrieval",
            "description": "Delete Entries From Collection",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_entries_from_collection_retrieval operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/retrieval/delete", json_data=json_data)

        self._log_execution_end(response)
        return response