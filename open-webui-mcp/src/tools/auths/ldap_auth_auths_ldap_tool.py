"""Ldap Auth"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class LdapAuthAuthsLdapTool(BaseTool):
    """Ldap Auth"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "ldap_auth_auths_ldap",
            "description": "Ldap Auth",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user": {
                        "type": "string",
                        "description": "LDAP username"
                    },
                    "password": {
                        "type": "string",
                        "description": "LDAP password"
                    }
                },
                "required": ["user", "password"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute ldap_auth_auths_ldap operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "user": arguments.get("user"),
            "password": arguments.get("password")
        }

        response = await self.client.post("/api/v1/auths/ldap", json_data=json_data)

        self._log_execution_end(response)
        return response