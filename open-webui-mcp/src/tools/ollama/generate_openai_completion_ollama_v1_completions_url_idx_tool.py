"""Generate Openai Completion"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateOpenaiCompletionOllamaV1CompletionsUrlIdxTool(BaseTool):
    """Generate Openai Completion"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_openai_completion_ollama_v1_completions_url_idx",
            "description": "Generate Openai Completion",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "integer",
                        "description": "Index of the Ollama URL to use"
                    },
                    "model": {
                        "type": "string",
                        "description": "Name of the model to use"
                    },
                    "prompt": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}}
                        ],
                        "description": "The prompt(s) to generate completions for"
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
                "required": ["url_idx", "model", "prompt"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_openai_completion_ollama_v1_completions_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request body - additionalProperties object
        json_data = {
            "model": arguments["model"],
            "prompt": arguments["prompt"]
        }
        optional_fields = ["max_tokens", "temperature", "top_p", "stream", "stop"]
        for field in optional_fields:
            if arguments.get(field) is not None:
                json_data[field] = arguments[field]
        # Pass through any additional properties
        for key, value in arguments.items():
            if key not in ["url_idx", "model", "prompt", "max_tokens", "temperature", "top_p", "stream", "stop"] and value is not None:
                json_data[key] = value

        response = await self.client.post(f"/ollama/v1/completions/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response