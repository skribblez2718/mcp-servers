"""Healthcheck With Db"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class HealthcheckWithDbHealthDbTool(BaseTool):
    """Healthcheck With Db"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "healthcheck_with_db_health_db",
            "description": "Healthcheck With Db",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute healthcheck_with_db_health_db operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/health/db", params=params)

        self._log_execution_end(response)
        return response