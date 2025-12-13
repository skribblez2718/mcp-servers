"""Get Current Usage"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetCurrentUsageUsageTool(BaseTool):
    """Get current usage statistics for Open WebUI. This is an experimental endpoint and subject to change."""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_current_usage_usage",
            "description": "Get current usage statistics for Open WebUI. This is an experimental endpoint and subject to change.",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_current_usage_usage operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/usage", params=params)

        self._log_execution_end(response)
        return response