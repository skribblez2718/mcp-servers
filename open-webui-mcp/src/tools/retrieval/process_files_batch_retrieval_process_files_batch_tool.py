"""Process Files Batch"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ProcessFilesBatchRetrievalProcessFilesBatchTool(BaseTool):
    """Process a batch of files and save them to the vector database."""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "process_files_batch_retrieval_process_files_batch",
            "description": "Process a batch of files and save them to the vector database.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "description": "Array of file objects to process",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "user_id": {"type": "string"},
                                "filename": {"type": "string"},
                                "hash": {"type": ["string", "null"]},
                                "path": {"type": ["string", "null"]},
                                "data": {"type": ["object", "null"]},
                                "meta": {"type": ["object", "null"]},
                                "access_control": {"type": ["object", "null"]},
                                "created_at": {"type": ["integer", "null"]},
                                "updated_at": {"type": ["integer", "null"]}
                            },
                            "required": ["id", "user_id", "filename", "created_at", "updated_at"]
                        }
                    },
                    "collection_name": {"type": "string", "description": "Collection name to store files in"}
                },
                "required": ["files", "collection_name"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute process_files_batch_retrieval_process_files_batch operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "files": arguments["files"],
            "collection_name": arguments["collection_name"]
        }

        response = await self.client.post("/api/v1/retrieval/process/files/batch", json_data=json_data)

        self._log_execution_end(response)
        return response