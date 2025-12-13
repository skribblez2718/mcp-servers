"""Create New Prompt"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewPromptPromptsCreateTool(BaseTool):
    """Create New Prompt"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_prompt_prompts_create",
            "description": "Create New Prompt",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_prompt_prompts_create operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/prompts/create", json_data=json_data)

        self._log_execution_end(response)
        return response