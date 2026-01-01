"""Delete Pipeline"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeletePipelinePipelinesTool(BaseTool):
    """Delete Pipeline"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_pipeline_pipelines",
            "description": "Delete Pipeline",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The ID of the pipeline to delete"
                    },
                    "urlIdx": {
                        "type": "integer",
                        "description": "The URL index of the pipeline server"
                    }
                },
                "required": ["id", "urlIdx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_pipeline_pipelines operation."""
        self._log_execution_start(arguments)

        # Build request - DELETE with JSON body
        json_data = {
            "id": arguments.get("id"),
            "urlIdx": arguments.get("urlIdx")
        }

        response = await self.client.delete_with_body("/api/v1/pipelines/delete", json_data=json_data)

        self._log_execution_end(response)
        return response