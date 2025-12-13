"""Health check tool for monitoring Recipez API availability."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class HealthCheckTool(BaseTool):
    """Check Recipez API health and readiness status."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_health_check"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Check Recipez API health and readiness status. "
            "Use 'health' for basic health check or 'ready' for readiness check."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "check_type": {
                    "type": "string",
                    "enum": ["health", "ready"],
                    "description": "Type of health check to perform",
                    "default": "health",
                }
            },
            "required": [],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute health check.

        Args:
            params: Dictionary with optional 'check_type' key

        Returns:
            Health check response from API
        """
        start = time.time()
        check_type = params.get("check_type", "health")
        endpoint = "/health" if check_type == "health" else "/health/ready"

        try:
            result = await self.http_client.get(endpoint)
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                check_type,
                duration,
                "success",
            )
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                check_type,
                duration,
                "error",
                error=str(e),
            )
            raise
