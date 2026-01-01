"""Upload Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UploadModelOllamaModelsUploadUrlIdxTool(BaseTool):
    """Upload Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "upload_model_ollama_models_upload_url_idx",
            "description": "Upload Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "integer",
                        "description": "Index of the Ollama URL to use"
                    },
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Model file to upload (binary data or file path)"
                    }
                },
                "required": ["url_idx", "file"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute upload_model_ollama_models_upload_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request - multipart/form-data with file
        # Note: This requires the client to handle file uploads
        files = {"file": arguments["file"]}

        response = await self.client.post(f"/ollama/models/upload/{url_idx}", files=files)

        self._log_execution_end(response)
        return response