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
                    "command": {
                        "type": "string",
                        "description": "The command/shortcut for the prompt (e.g., 'summarize')"
                    },
                    "title": {
                        "type": "string",
                        "description": "The title of the prompt"
                    },
                    "content": {
                        "type": "string",
                        "description": "The prompt content/template"
                    },
                    "access_control": {
                        "type": "object",
                        "description": "Optional access control settings",
                        "additionalProperties": True
                    }
                },
                "required": ["command", "title", "content"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_prompt_prompts_create operation."""
        self._log_execution_start(arguments)

        # Build request body per PromptForm schema
        json_data = {
            "command": arguments.get("command"),
            "title": arguments.get("title"),
            "content": arguments.get("content")
        }
        # Add optional access_control if provided
        if arguments.get("access_control") is not None:
            json_data["access_control"] = arguments.get("access_control")

        response = await self.client.post("/api/v1/prompts/create", json_data=json_data)

        self._log_execution_end(response)
        return response