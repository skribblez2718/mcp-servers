"""Generate Follow Ups"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateFollowUpsTasksFollowUpCompletionsTool(BaseTool):
    """Generate Follow Ups"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_follow_ups_tasks_follow_up_completions",
            "description": "Generate Follow Ups",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_follow_ups_tasks_follow_up_completions operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/tasks/follow_up/completions", json_data=json_data)

        self._log_execution_end(response)
        return response