"""Admin health check tool."""

from typing import Any
from src.tools.base import BaseTool


class AdminHealthTool(BaseTool):
    """Check Open WebUI instance health status.

    Returns health information and system status.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition with schema
        """
        return {
            "name": "admin_health",
            "description": "Check Open WebUI instance health and status",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute health check.

        Args:
            arguments: Tool arguments (none required)

        Returns:
            Health status dict

        Raises:
            HTTPError: If API call fails
        """
        self._log_execution_start(arguments)

        # Call health endpoint
        response_data = await self.client.get("/health")

        result = {
            "status": response_data.get("status", "unknown"),
            "timestamp": response_data.get("timestamp"),
            "details": response_data
        }

        self._log_execution_end(result)

        return result
