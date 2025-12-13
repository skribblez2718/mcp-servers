"""Get Pipelines"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetPipelinesPipelinesTool(BaseTool):
    """Get Pipelines"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_pipelines_pipelines",
            "description": "Get Pipelines",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "urlIdx": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_pipelines_pipelines operation."""
        self._log_execution_start(arguments)


        # Query parameter: urlIdx
        urlIdx = arguments.get("urlIdx")

        # Build request
        params = {}
        if urlIdx is not None:
            params["urlIdx"] = urlIdx

        response = await self.client.get("/api/v1/pipelines/", params=params)

        self._log_execution_end(response)
        return response