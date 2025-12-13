"""Healthcheck"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class HealthcheckHealthTool(BaseTool):
    """Healthcheck"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "healthcheck_health",
            "description": "Healthcheck",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute healthcheck_health operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/health", params=params)

        self._log_execution_end(response)
        return response