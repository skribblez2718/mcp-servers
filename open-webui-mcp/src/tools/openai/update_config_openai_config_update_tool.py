"""Update Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateConfigOpenaiConfigUpdateTool(BaseTool):
    """Update Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_config_openai_config_update",
            "description": "Update Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ENABLE_OPENAI_API": {"type": ["boolean", "null"], "description": "Enable OpenAI API (optional)"},
                    "OPENAI_API_BASE_URLS": {"type": "array", "items": {"type": "string"}, "description": "List of OpenAI API base URLs"},
                    "OPENAI_API_KEYS": {"type": "array", "items": {"type": "string"}, "description": "List of OpenAI API keys"},
                    "OPENAI_API_CONFIGS": {"type": "object", "additionalProperties": True, "description": "Additional API configurations"}
                },
                "required": ["OPENAI_API_BASE_URLS", "OPENAI_API_KEYS", "OPENAI_API_CONFIGS"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_config_openai_config_update operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "OPENAI_API_BASE_URLS": arguments.get("OPENAI_API_BASE_URLS"),
            "OPENAI_API_KEYS": arguments.get("OPENAI_API_KEYS"),
            "OPENAI_API_CONFIGS": arguments.get("OPENAI_API_CONFIGS")
        }
        if arguments.get("ENABLE_OPENAI_API") is not None:
            json_data["ENABLE_OPENAI_API"] = arguments.get("ENABLE_OPENAI_API")

        response = await self.client.post("/openai/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response