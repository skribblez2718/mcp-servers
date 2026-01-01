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
                    "label": {
                        "type": "string",
                        "description": "LDAP server label"
                    },
                    "host": {
                        "type": "string",
                        "description": "LDAP server hostname"
                    },
                    "port": {
                        "type": ["integer", "null"],
                        "description": "LDAP server port"
                    },
                    "attribute_for_mail": {
                        "type": "string",
                        "description": "LDAP attribute for email",
                        "default": "mail"
                    },
                    "attribute_for_username": {
                        "type": "string",
                        "description": "LDAP attribute for username",
                        "default": "uid"
                    },
                    "app_dn": {
                        "type": "string",
                        "description": "Application Distinguished Name"
                    },
                    "app_dn_password": {
                        "type": "string",
                        "description": "Application DN password"
                    },
                    "search_base": {
                        "type": "string",
                        "description": "LDAP search base"
                    },
                    "search_filters": {
                        "type": "string",
                        "description": "LDAP search filters",
                        "default": ""
                    },
                    "use_tls": {
                        "type": "boolean",
                        "description": "Use TLS for connection",
                        "default": True
                    },
                    "certificate_path": {
                        "type": ["string", "null"],
                        "description": "Path to TLS certificate"
                    },
                    "validate_cert": {
                        "type": "boolean",
                        "description": "Validate TLS certificate",
                        "default": True
                    },
                    "ciphers": {
                        "type": ["string", "null"],
                        "description": "TLS ciphers to use",
                        "default": "ALL"
                    }
                },
                "required": ["label", "host", "app_dn", "app_dn_password", "search_base"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_ldap_server_auths_admin_config_ldap_server operation."""
        self._log_execution_start(arguments)



        # Build request - required fields
        json_data = {
            "label": arguments.get("label"),
            "host": arguments.get("host"),
            "app_dn": arguments.get("app_dn"),
            "app_dn_password": arguments.get("app_dn_password"),
            "search_base": arguments.get("search_base")
        }
        # Add optional fields if provided
        if arguments.get("port") is not None:
            json_data["port"] = arguments.get("port")
        if arguments.get("attribute_for_mail") is not None:
            json_data["attribute_for_mail"] = arguments.get("attribute_for_mail")
        if arguments.get("attribute_for_username") is not None:
            json_data["attribute_for_username"] = arguments.get("attribute_for_username")
        if arguments.get("search_filters") is not None:
            json_data["search_filters"] = arguments.get("search_filters")
        if arguments.get("use_tls") is not None:
            json_data["use_tls"] = arguments.get("use_tls")
        if arguments.get("certificate_path") is not None:
            json_data["certificate_path"] = arguments.get("certificate_path")
        if arguments.get("validate_cert") is not None:
            json_data["validate_cert"] = arguments.get("validate_cert")
        if arguments.get("ciphers") is not None:
            json_data["ciphers"] = arguments.get("ciphers")

        response = await self.client.post("/api/v1/auths/admin/config/ldap/server", json_data=json_data)

        self._log_execution_end(response)
        return response