"""Generate Chat Completion"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateChatCompletionOllamaChatTool(BaseTool):
    """Generate Chat Completion"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_chat_completion_ollama_chat",
            "description": "Generate Chat Completion",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": ["integer", "null"],
                        "description": "Index of the Ollama URL to use"
                    },
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
                    "format": {
                        "oneOf": [
                            {"type": "object"},
                            {"type": "string"},
                            {"type": "null"}
                        ],
                        "description": "Response format (e.g., 'json')"
                    },
                    "options": {
                        "type": ["object", "null"],
                        "description": "Additional model parameters"
                    },
                    "stream": {
                        "type": ["boolean", "null"],
                        "description": "Stream the response"
                    },
                    "keep_alive": {
                        "oneOf": [
                            {"type": "integer"},
                            {"type": "string"},
                            {"type": "null"}
                        ],
                        "description": "How long to keep the model loaded"
                    }
                },
                "required": ["model", "messages"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_chat_completion_ollama_chat operation."""
        self._log_execution_start(arguments)


        # Query parameters
        params = {}
        url_idx = arguments.get("url_idx")
        if url_idx is not None:
            params["url_idx"] = url_idx
        bypass_filter = arguments.get("bypass_filter", False)
        if bypass_filter is not None:
            params["bypass_filter"] = bypass_filter

        # Build request body - additionalProperties object (pass through all body params)
        json_data = {
            "model": arguments["model"],
            "messages": arguments["messages"]
        }
        optional_fields = ["format", "options", "stream", "keep_alive"]
        for field in optional_fields:
            if arguments.get(field) is not None:
                json_data[field] = arguments[field]
        # Pass through any additional properties
        for key, value in arguments.items():
            if key not in ["url_idx", "bypass_filter", "model", "messages", "format", "options", "stream", "keep_alive"] and value is not None:
                json_data[key] = value

        response = await self.client.post("/ollama/api/chat", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response