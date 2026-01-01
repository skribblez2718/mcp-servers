"""Upload Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UploadModelOllamaModelsUploadTool(BaseTool):
    """Upload Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "upload_model_ollama_models_upload",
            "description": "Upload Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": ["integer", "null"],
                        "description": "Index of the Ollama URL to use"
                    },
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Model file to upload (binary data or file path)"
                    }
                },
                "required": ["file"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute upload_model_ollama_models_upload operation."""
        self._log_execution_start(arguments)


        # Query parameter: url_idx
        params = {}
        url_idx = arguments.get("url_idx")
        if url_idx is not None:
            params["url_idx"] = url_idx

        # Build request - multipart/form-data with file
        # Note: This requires the client to handle file uploads
        files = {"file": arguments["file"]}

        response = await self.client.post("/ollama/models/upload", files=files, params=params)

        self._log_execution_end(response)
        return response