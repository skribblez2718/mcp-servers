"""Get Gravatar"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetGravatarUtilsGravatarTool(BaseTool):
    """Get Gravatar"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_gravatar_utils_gravatar",
            "description": "Get Gravatar",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["email"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_gravatar_utils_gravatar operation."""
        self._log_execution_start(arguments)


        # Query parameter: email
        email = arguments.get("email")

        # Build request
        params = {}
        if email is not None:
            params["email"] = email

        response = await self.client.get("/api/v1/utils/gravatar", params=params)

        self._log_execution_end(response)
        return response