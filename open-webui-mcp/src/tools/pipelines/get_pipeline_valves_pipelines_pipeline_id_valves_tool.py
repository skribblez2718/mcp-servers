"""Get Pipeline Valves"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetPipelineValvesPipelinesPipelineIdValvesTool(BaseTool):
    """Get Pipeline Valves"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_pipeline_valves_pipelines_pipeline_id_valves",
            "description": "Get Pipeline Valves",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "pipeline_id": {
                        "type": "string",
                        "description": ""
                    },
                    "urlIdx": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["pipeline_id", "urlIdx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_pipeline_valves_pipelines_pipeline_id_valves operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: pipeline_id
        pipeline_id = arguments.get("pipeline_id")
        if pipeline_id:
            pipeline_id = ToolInputValidator.validate_id(pipeline_id, "pipeline_id")

        # Query parameter: urlIdx
        urlIdx = arguments.get("urlIdx")

        # Build request
        params = {}
        if urlIdx is not None:
            params["urlIdx"] = urlIdx

        response = await self.client.get(f"/api/v1/pipelines/{pipeline_id}/valves", params=params)

        self._log_execution_end(response)
        return response