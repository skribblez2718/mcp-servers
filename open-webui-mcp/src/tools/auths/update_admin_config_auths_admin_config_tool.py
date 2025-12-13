"""Update Admin Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateAdminConfigAuthsAdminConfigTool(BaseTool):
    """Update Admin Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_admin_config_auths_admin_config",
            "description": "Update Admin Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_admin_config_auths_admin_config operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/auths/admin/config", json_data=json_data)

        self._log_execution_end(response)
        return response