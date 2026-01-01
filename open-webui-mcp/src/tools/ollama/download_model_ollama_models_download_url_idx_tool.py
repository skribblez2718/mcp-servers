"""Download Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DownloadModelOllamaModelsDownloadUrlIdxTool(BaseTool):
    """Download Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "download_model_ollama_models_download_url_idx",
            "description": "Download Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "integer",
                        "description": "Index of the Ollama URL to use"
                    },
                    "url": {
                        "type": "string",
                        "description": "URL of the model to download"
                    }
                },
                "required": ["url_idx", "url"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute download_model_ollama_models_download_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request body - UrlForm
        json_data = {
            "url": arguments["url"]
        }

        response = await self.client.post(f"/ollama/models/download/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response