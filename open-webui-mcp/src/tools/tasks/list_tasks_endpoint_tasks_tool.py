"""List Tasks Endpoint"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ListTasksEndpointTasksTool(BaseTool):
    """List Tasks Endpoint"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "list_tasks_endpoint_tasks",
            "description": "List Tasks Endpoint",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute list_tasks_endpoint_tasks operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/tasks", params=params)

        self._log_execution_end(response)
        return response