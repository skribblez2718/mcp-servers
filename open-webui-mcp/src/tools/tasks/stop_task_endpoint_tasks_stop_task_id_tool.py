"""Stop Task Endpoint"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class StopTaskEndpointTasksStopTaskIdTool(BaseTool):
    """Stop Task Endpoint"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "stop_task_endpoint_tasks_stop_task_id",
            "description": "Stop Task Endpoint",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["task_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute stop_task_endpoint_tasks_stop_task_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: task_id
        task_id = arguments.get("task_id")
        if task_id:
            task_id = ToolInputValidator.validate_id(task_id, "task_id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/tasks/stop/{task_id}", json_data=json_data)

        self._log_execution_end(response)
        return response