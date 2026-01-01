"""Generate Completion"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GenerateCompletionOllamaGenerateUrlIdxTool(BaseTool):
    """Generate Completion"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "generate_completion_ollama_generate_url_idx",
            "description": "Generate Completion",
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
                        "type": "string",
                        "description": "The prompt to generate a response for"
                    },
                    "suffix": {
                        "type": ["string", "null"],
                        "description": "Text after the model response"
                    },
                    "images": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "Base64-encoded images for multimodal models"
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
                    "system": {
                        "type": ["string", "null"],
                        "description": "System prompt override"
                    },
                    "template": {
                        "type": ["string", "null"],
                        "description": "Prompt template override"
                    },
                    "context": {
                        "type": ["array", "null"],
                        "items": {"type": "integer"},
                        "description": "Context from a previous response"
                    },
                    "stream": {
                        "type": ["boolean", "null"],
                        "description": "Stream the response",
                        "default": True
                    },
                    "raw": {
                        "type": ["boolean", "null"],
                        "description": "Raw mode - no formatting"
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
                "required": ["url_idx", "model", "prompt"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute generate_completion_ollama_generate_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request body - GenerateCompletionForm
        json_data = {
            "model": arguments["model"],
            "prompt": arguments["prompt"]
        }
        optional_fields = ["suffix", "images", "format", "options", "system", "template", "context", "stream", "raw", "keep_alive"]
        for field in optional_fields:
            if arguments.get(field) is not None:
                json_data[field] = arguments[field]

        response = await self.client.post(f"/ollama/api/generate/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response