"""Get Ldap Server"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetLdapServerAuthsAdminConfigLdapServerTool(BaseTool):
    """Get Ldap Server"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_ldap_server_auths_admin_config_ldap_server",
            "description": "Get Ldap Server",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_ldap_server_auths_admin_config_ldap_server operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/auths/admin/config/ldap/server", params=params)

        self._log_execution_end(response)
        return response