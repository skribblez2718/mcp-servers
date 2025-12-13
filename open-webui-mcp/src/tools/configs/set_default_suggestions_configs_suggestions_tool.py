"""Set Default Suggestions"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetDefaultSuggestionsConfigsSuggestionsTool(BaseTool):
    """Set Default Suggestions"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_default_suggestions_configs_suggestions",
            "description": "Set Default Suggestions",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_default_suggestions_configs_suggestions operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/configs/suggestions", json_data=json_data)

        self._log_execution_end(response)
        return response