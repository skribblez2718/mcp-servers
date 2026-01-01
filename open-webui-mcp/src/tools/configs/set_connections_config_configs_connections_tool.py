"""Set Connections Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetConnectionsConfigConfigsConnectionsTool(BaseTool):
    """Set Connections Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_connections_config_configs_connections",
            "description": "Set Connections Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ENABLE_DIRECT_CONNECTIONS": {
                        "type": "boolean",
                        "description": "Enable direct connections to models"
                    },
                    "ENABLE_BASE_MODELS_CACHE": {
                        "type": "boolean",
                        "description": "Enable caching of base models"
                    }
                },
                "required": ["ENABLE_DIRECT_CONNECTIONS", "ENABLE_BASE_MODELS_CACHE"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_connections_config_configs_connections operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "ENABLE_DIRECT_CONNECTIONS": arguments.get("ENABLE_DIRECT_CONNECTIONS"),
            "ENABLE_BASE_MODELS_CACHE": arguments.get("ENABLE_BASE_MODELS_CACHE")
        }

        response = await self.client.post("/api/v1/configs/connections", json_data=json_data)

        self._log_execution_end(response)
        return response