"""Update Task Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateTaskConfigTasksConfigUpdateTool(BaseTool):
    """Update Task Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_task_config_tasks_config_update",
            "description": "Update Task Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_task_config_tasks_config_update operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/tasks/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response