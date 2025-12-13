"""Reset Upload Dir"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ResetUploadDirRetrievalResetUploadsTool(BaseTool):
    """Reset Upload Dir"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "reset_upload_dir_retrieval_reset_uploads",
            "description": "Reset Upload Dir",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute reset_upload_dir_retrieval_reset_uploads operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/retrieval/reset/uploads", json_data=json_data)

        self._log_execution_end(response)
        return response