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
                        "type": ["boolean", "null"],
                        "description": "Bypass content filter",
                        "default": False
                    },
                    "model": {
                        "type": "string",
                        "description": "Name of the model to use"
                    },
                    "messages": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Array of message objects with role and content"
                    },
                    "max_tokens": {
                        "type": ["integer", "null"],
                        "description": "Maximum tokens to generate"
                    },
                    "temperature": {
                        "type": ["number", "null"],
                        "description": "Sampling temperature"
                    },
                    "top_p": {
                        "type": ["number", "null"],
                        "description": "Nucleus sampling parameter"
                    },
                    "stream": {
                        "type": ["boolean", "null"],
                        "description": "Stream the response"
                    },
                    "stop": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "null"}
                        ],
                        "description": "Stop sequences"
                    }
                },
                "required": ["model", "messages"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_chat_completion_openai_chat_completions operation."""
        self._log_execution_start(arguments)


        # Query parameter: bypass_filter
        params = {}
        bypass_filter = arguments.get("bypass_filter", False)
        if bypass_filter is not None:
            params["bypass_filter"] = bypass_filter

        # Build request body - additionalProperties object
        json_data = {
            "model": arguments["model"],
            "messages": arguments["messages"]
        }
        optional_fields = ["max_tokens", "temperature", "top_p", "stream", "stop"]
        for field in optional_fields:
            if arguments.get(field) is not None:
                json_data[field] = arguments[field]
        # Pass through any additional properties
        for key, value in arguments.items():
            if key not in ["bypass_filter", "model", "messages", "max_tokens", "temperature", "top_p", "stream", "stop"] and value is not None:
                json_data[key] = value

        response = await self.client.post("/openai/chat/completions", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response