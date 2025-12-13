"""Generate Chat Completion"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateChatCompletionOllamaChatUrlIdxTool(BaseTool):
    """Generate Chat Completion"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_chat_completion_ollama_chat_url_idx",
            "description": "Generate Chat Completion",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "string",
                        "description": ""
                    },
                    "bypass_filter": {
                        "type": "string",
                        "description": "",
                        "default": False
                    }
                },
                "required": ["url_idx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_chat_completion_ollama_chat_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")

        # Query parameter: bypass_filter
        bypass_filter = arguments.get("bypass_filter", False)

        # Build request
        json_data = {}

        response = await self.client.post(f"/ollama/api/chat/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response