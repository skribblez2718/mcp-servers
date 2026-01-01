"""Verify Tool Servers Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class VerifyToolServersConfigConfigsToolServersVerifyTool(BaseTool):
    """Verify the connection to the tool server."""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "verify_tool_servers_config_configs_tool_servers_verify",
            "description": "Verify the connection to the tool server.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the tool server"
                    },
                    "path": {
                        "type": "string",
                        "description": "The path on the tool server"
                    },
                    "auth_type": {
                        "type": ["string", "null"],
                        "description": "The authentication type (optional)"
                    },
                    "key": {
                        "type": ["string", "null"],
                        "description": "The authentication key (optional)"
                    },
                    "config": {
                        "type": ["object", "null"],
                        "additionalProperties": True,
                        "description": "Additional configuration (optional)"
                    }
                },
                "required": ["url", "path", "auth_type", "key", "config"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute verify_tool_servers_config_configs_tool_servers_verify operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "url": arguments.get("url"),
            "path": arguments.get("path"),
            "auth_type": arguments.get("auth_type"),
            "key": arguments.get("key"),
            "config": arguments.get("config")
        }

        response = await self.client.post("/api/v1/configs/tool_servers/verify", json_data=json_data)

        self._log_execution_end(response)
        return response