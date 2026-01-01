"""Set Tool Servers Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetToolServersConfigConfigsToolServersTool(BaseTool):
    """Set Tool Servers Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_tool_servers_config_configs_tool_servers",
            "description": "Set Tool Servers Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "TOOL_SERVER_CONNECTIONS": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string"},
                                "path": {"type": "string"},
                                "auth_type": {"type": ["string", "null"]},
                                "key": {"type": ["string", "null"]},
                                "config": {"type": ["object", "null"], "additionalProperties": True}
                            },
                            "required": ["url", "path", "auth_type", "key", "config"]
                        },
                        "description": "Array of tool server connection configurations"
                    }
                },
                "required": ["TOOL_SERVER_CONNECTIONS"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_tool_servers_config_configs_tool_servers operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "TOOL_SERVER_CONNECTIONS": arguments.get("TOOL_SERVER_CONNECTIONS", [])
        }

        response = await self.client.post("/api/v1/configs/tool_servers", json_data=json_data)

        self._log_execution_end(response)
        return response