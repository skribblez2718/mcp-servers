"""Download Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DownloadModelOllamaModelsDownloadTool(BaseTool):
    """Download Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "download_model_ollama_models_download",
            "description": "Download Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": ["integer", "null"],
                        "description": "Index of the Ollama URL to use"
                    },
                    "url": {
                        "type": "string",
                        "description": "URL of the model to download"
                    }
                },
                "required": ["url"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute download_model_ollama_models_download operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        params = {}
        url_idx = arguments.get("url_idx")
        if url_idx is not None:
            params["url_idx"] = url_idx

        # Build request body - UrlForm
        json_data = {
            "url": arguments["url"]
        }

        response = await self.client.post("/ollama/models/download", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response