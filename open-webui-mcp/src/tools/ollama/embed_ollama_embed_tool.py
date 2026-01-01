"""Embed"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class EmbedOllamaEmbedTool(BaseTool):
    """Embed"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "embed_ollama_embed",
            "description": "Embed",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": ["integer", "null"],
                        "description": "Index of the Ollama URL to use"
                    },
                    "model": {
                        "type": "string",
                        "description": "Name of the model to use for embedding"
                    },
                    "input": {
                        "oneOf": [
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "string"}
                        ],
                        "description": "Text(s) to embed - can be a string or array of strings"
                    },
                    "truncate": {
                        "type": ["boolean", "null"],
                        "description": "Whether to truncate the input"
                    },
                    "options": {
                        "type": ["object", "null"],
                        "description": "Additional model options"
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
                "required": ["model", "input"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute embed_ollama_embed operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        url_idx = arguments.get("url_idx")
        params = {}
        if url_idx is not None:
            params["url_idx"] = url_idx

        # Build request body - GenerateEmbedForm
        json_data = {
            "model": arguments["model"],
            "input": arguments["input"]
        }
        if arguments.get("truncate") is not None:
            json_data["truncate"] = arguments["truncate"]
        if arguments.get("options") is not None:
            json_data["options"] = arguments["options"]
        if arguments.get("keep_alive") is not None:
            json_data["keep_alive"] = arguments["keep_alive"]

        response = await self.client.post("/ollama/api/embed", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response