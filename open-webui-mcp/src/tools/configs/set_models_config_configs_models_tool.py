"""Set Models Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetModelsConfigConfigsModelsTool(BaseTool):
    """Set Models Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_models_config_configs_models",
            "description": "Set Models Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "DEFAULT_MODELS": {
                        "type": ["string", "null"],
                        "description": "Default models to use"
                    },
                    "DEFAULT_PINNED_MODELS": {
                        "type": ["string", "null"],
                        "description": "Default pinned models (not in spec but required by server)"
                    },
                    "MODEL_ORDER_LIST": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "Ordered list of model IDs"
                    }
                },
                "required": ["DEFAULT_MODELS", "DEFAULT_PINNED_MODELS", "MODEL_ORDER_LIST"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_models_config_configs_models operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "DEFAULT_MODELS": arguments.get("DEFAULT_MODELS"),
            "DEFAULT_PINNED_MODELS": arguments.get("DEFAULT_PINNED_MODELS"),
            "MODEL_ORDER_LIST": arguments.get("MODEL_ORDER_LIST")
        }

        response = await self.client.post("/api/v1/configs/models", json_data=json_data)

        self._log_execution_end(response)
        return response