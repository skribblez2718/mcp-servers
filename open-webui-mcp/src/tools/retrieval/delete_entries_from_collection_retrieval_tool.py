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
            "description": "Delete entries from a collection",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string", "description": "Collection name to delete from"},
                    "file_id": {"type": "string", "description": "File ID to delete"}
                },
                "required": ["collection_name", "file_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_entries_from_collection_retrieval operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "collection_name": arguments["collection_name"],
            "file_id": arguments["file_id"]
        }

        response = await self.client.post("/api/v1/retrieval/delete", json_data=json_data)

        self._log_execution_end(response)
        return response