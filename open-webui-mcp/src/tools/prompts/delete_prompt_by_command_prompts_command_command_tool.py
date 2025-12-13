"""Delete Prompt By Command"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeletePromptByCommandPromptsCommandCommandTool(BaseTool):
    """Delete Prompt By Command"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_prompt_by_command_prompts_command_command",
            "description": "Delete Prompt By Command",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["command"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_prompt_by_command_prompts_command_command operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: command
        command = arguments.get("command")
        if command:
            command = ToolInputValidator.validate_id(command, "command")


        # Build request
        params = {}

        response = await self.client.delete(f"/api/v1/prompts/command/{command}/delete", params=params)

        self._log_execution_end(response)
        return response