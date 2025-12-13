"""Download Db"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DownloadDbUtilsDbDownloadTool(BaseTool):
    """Download Db"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "download_db_utils_db_download",
            "description": "Download Db",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute download_db_utils_db_download operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/utils/db/download", params=params)

        self._log_execution_end(response)
        return response