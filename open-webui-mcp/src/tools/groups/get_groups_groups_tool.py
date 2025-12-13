"""Get Groups"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetGroupsGroupsTool(BaseTool):
    """Get Groups"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_groups_groups",
            "description": "Get Groups",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_groups_groups operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/groups/", params=params)

        self._log_execution_end(response)
        return response