"""Update Ldap Server"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateLdapServerAuthsAdminConfigLdapServerTool(BaseTool):
    """Update Ldap Server"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_ldap_server_auths_admin_config_ldap_server",
            "description": "Update Ldap Server",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_ldap_server_auths_admin_config_ldap_server operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/auths/admin/config/ldap/server", json_data=json_data)

        self._log_execution_end(response)
        return response