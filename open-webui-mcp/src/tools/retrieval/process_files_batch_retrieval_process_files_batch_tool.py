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
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute process_files_batch_retrieval_process_files_batch operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/retrieval/process/files/batch", json_data=json_data)

        self._log_execution_end(response)
        return response