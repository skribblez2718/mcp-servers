"""Update Prompt By Command"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdatePromptByCommandPromptsCommandCommandUpdateTool(BaseTool):
    """Update Prompt By Command"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_prompt_by_command_prompts_command_command_update",
            "description": "Update Prompt By Command",
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
        """Execute update_prompt_by_command_prompts_command_command_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: command
        command = arguments.get("command")
        if command:
            command = ToolInputValidator.validate_id(command, "command")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/prompts/command/{command}/update", json_data=json_data)

        self._log_execution_end(response)
        return response