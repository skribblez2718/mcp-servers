"""Update Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateConfigOllamaConfigUpdateTool(BaseTool):
    """Update Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_config_ollama_config_update",
            "description": "Update Ollama Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ENABLE_OLLAMA_API": {"type": ["boolean", "null"], "description": "Enable Ollama API"},
                    "OLLAMA_BASE_URLS": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of Ollama base URLs"
                    },
                    "OLLAMA_API_CONFIGS": {
                        "type": "object",
                        "additionalProperties": True,
                        "description": "Ollama API configurations"
                    }
                },
                "required": ["OLLAMA_BASE_URLS", "OLLAMA_API_CONFIGS"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_config_ollama_config_update operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "OLLAMA_BASE_URLS": arguments["OLLAMA_BASE_URLS"],
            "OLLAMA_API_CONFIGS": arguments["OLLAMA_API_CONFIGS"]
        }
        if arguments.get("ENABLE_OLLAMA_API") is not None:
            json_data["ENABLE_OLLAMA_API"] = arguments["ENABLE_OLLAMA_API"]

        response = await self.client.post("/ollama/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response