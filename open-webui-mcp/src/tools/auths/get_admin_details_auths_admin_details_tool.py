"""Get Admin Details"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetAdminDetailsAuthsAdminDetailsTool(BaseTool):
    """Get Admin Details"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_admin_details_auths_admin_details",
            "description": "Get Admin Details",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_admin_details_auths_admin_details operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/auths/admin/details", params=params)

        self._log_execution_end(response)
        return response