"""Delete Api Key"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteKeyAuthsKeyTool(BaseTool):
    """Delete Api Key"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_key_auths_key",
            "description": "Delete Api Key",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_key_auths_key operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.delete("/api/v1/auths/api_key", params=params)

        self._log_execution_end(response)
        return response