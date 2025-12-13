"""Get Models"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetModelsModelsTool(BaseTool):
    """Get Models"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_models_models",
            "description": "Get Models",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "boolean",
                        "description": "",
                        "default": False
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_models_models operation."""
        self._log_execution_start(arguments)


        # Query parameter: refresh
        refresh = arguments.get("refresh", False)

        # Build request
        params = {}
        if refresh is not None:
            params["refresh"] = refresh

        response = await self.client.get("/api/models", params=params)

        self._log_execution_end(response)
        return response