"""Generate Openai Chat Completion"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateOpenaiChatCompletionOllamaV1ChatCompletionsUrlIdxTool(BaseTool):
    """Generate Openai Chat Completion"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_openai_chat_completion_ollama_v1_chat_completions_url_idx",
            "description": "Generate Openai Chat Completion",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["url_idx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_openai_chat_completion_ollama_v1_chat_completions_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request
        json_data = {}

        response = await self.client.post(f"/ollama/v1/chat/completions/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response