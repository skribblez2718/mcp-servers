"""Generate Title"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateTitleTasksTitleCompletionsTool(BaseTool):
    """Generate Title"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_title_tasks_title_completions",
            "description": "Generate Title",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_title_tasks_title_completions operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/tasks/title/completions", json_data=json_data)

        self._log_execution_end(response)
        return response