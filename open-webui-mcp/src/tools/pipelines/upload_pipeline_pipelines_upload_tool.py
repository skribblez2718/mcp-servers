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
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute upload_pipeline_pipelines_upload operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/pipelines/upload", json_data=json_data)

        self._log_execution_end(response)
        return response