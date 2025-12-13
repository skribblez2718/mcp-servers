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
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_tool_servers_config_configs_tool_servers operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/configs/tool_servers", json_data=json_data)

        self._log_execution_end(response)
        return response