"""Add Pipeline"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class AddPipelinePipelinesAddTool(BaseTool):
    """Add Pipeline"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "add_pipeline_pipelines_add",
            "description": "Add Pipeline",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute add_pipeline_pipelines_add operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/pipelines/add", json_data=json_data)

        self._log_execution_end(response)
        return response