"""Upload Pipeline"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UploadPipelinePipelinesUploadTool(BaseTool):
    """Upload Pipeline"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "upload_pipeline_pipelines_upload",
            "description": "Upload Pipeline",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "urlIdx": {
                        "type": "integer",
                        "description": "The URL index of the pipeline server"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path to the pipeline file to upload"
                    }
                },
                "required": ["urlIdx", "file_path"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute upload_pipeline_pipelines_upload operation."""
        self._log_execution_start(arguments)

        file_path = arguments.get("file_path")
        urlIdx = arguments.get("urlIdx")

        # Build request with multipart/form-data
        form_data = {
            "urlIdx": urlIdx
        }

        response = await self.client.post_with_file("/api/v1/pipelines/upload", file_path, form_data=form_data)

        self._log_execution_end(response)
        return response