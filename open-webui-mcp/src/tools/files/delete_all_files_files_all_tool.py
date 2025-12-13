"""Delete All Files"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteAllFilesFilesAllTool(BaseTool):
    """Delete All Files"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_all_files_files_all",
            "description": "Delete All Files",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_all_files_files_all operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.delete("/api/v1/files/all", params=params)

        self._log_execution_end(response)
        return response