"""Generate Chat Completion"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateChatCompletionOpenaiChatCompletionsTool(BaseTool):
    """Generate Chat Completion"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_chat_completion_openai_chat_completions",
            "description": "Generate Chat Completion",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "bypass_filter": {
                        "type": "string",
                        "description": "",
                        "default": False
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_chat_completion_openai_chat_completions operation."""
        self._log_execution_start(arguments)


        # Query parameter: bypass_filter
        bypass_filter = arguments.get("bypass_filter", False)

        # Build request
        json_data = {}

        response = await self.client.post("/openai/chat/completions", json_data=json_data)

        self._log_execution_end(response)
        return response