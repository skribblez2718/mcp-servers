"""Get App Latest Release Version"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetAppLatestReleaseVersionVersionUpdatesTool(BaseTool):
    """Get App Latest Release Version"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_app_latest_release_version_version_updates",
            "description": "Get App Latest Release Version",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_app_latest_release_version_version_updates operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/version/updates", params=params)

        self._log_execution_end(response)
        return response