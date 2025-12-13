"""Download Chat As Pdf"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DownloadChatAsPdfUtilsPdfTool(BaseTool):
    """Download Chat As Pdf"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "download_chat_as_pdf_utils_pdf",
            "description": "Download Chat As Pdf",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute download_chat_as_pdf_utils_pdf operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/utils/pdf", json_data=json_data)

        self._log_execution_end(response)
        return response