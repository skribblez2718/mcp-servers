"""Process File"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ProcessFileRetrievalProcessFileTool(BaseTool):
    """Process File"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "process_file_retrieval_process_file",
            "description": "Process File for RAG retrieval",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_id": {"type": "string", "description": "File ID to process"},
                    "content": {"type": ["string", "null"], "description": "Optional content override"},
                    "collection_name": {"type": ["string", "null"], "description": "Collection name to store in"}
                },
                "required": ["file_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute process_file_retrieval_process_file operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {"file_id": arguments["file_id"]}
        if arguments.get("content") is not None:
            json_data["content"] = arguments["content"]
        if arguments.get("collection_name") is not None:
            json_data["collection_name"] = arguments["collection_name"]

        response = await self.client.post("/api/v1/retrieval/process/file", json_data=json_data)

        self._log_execution_end(response)
        return response