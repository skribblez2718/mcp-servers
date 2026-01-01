"""Copy Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CopyModelOllamaCopyUrlIdxTool(BaseTool):
    """Copy Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "copy_model_ollama_copy_url_idx",
            "description": "Copy Model in specific Ollama instance",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {"type": ["integer", "null"], "description": "URL index"},
                    "source": {"type": "string", "description": "Source model name"},
                    "destination": {"type": "string", "description": "Destination model name"}
                },
                "required": ["url_idx", "source", "destination"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute copy_model_ollama_copy_url_idx operation."""
        self._log_execution_start(arguments)

        # Path parameter: url_idx
        url_idx = arguments.get("url_idx")

        # Build request - CopyModelForm
        json_data = {
            "source": arguments["source"],
            "destination": arguments["destination"]
        }

        response = await self.client.post(f"/ollama/api/copy/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response