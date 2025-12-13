"""Generate Image Prompt"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateImagePromptTasksImagePromptCompletionsTool(BaseTool):
    """Generate Image Prompt"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_image_prompt_tasks_image_prompt_completions",
            "description": "Generate Image Prompt",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_image_prompt_tasks_image_prompt_completions operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/tasks/image_prompt/completions", json_data=json_data)

        self._log_execution_end(response)
        return response