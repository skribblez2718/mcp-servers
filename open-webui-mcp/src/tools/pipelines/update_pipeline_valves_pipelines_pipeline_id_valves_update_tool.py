"""Update Pipeline Valves"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdatePipelineValvesPipelinesPipelineIdValvesUpdateTool(BaseTool):
    """Update Pipeline Valves"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_pipeline_valves_pipelines_pipeline_id_valves_update",
            "description": "Update Pipeline Valves",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "pipeline_id": {
                        "type": "string",
                        "description": "The ID of the pipeline"
                    },
                    "urlIdx": {
                        "type": "string",
                        "description": "The URL index of the pipeline server"
                    },
                    "valves": {
                        "type": "object",
                        "description": "The valve configuration data to update",
                        "additionalProperties": True
                    }
                },
                "required": ["pipeline_id", "urlIdx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_pipeline_valves_pipelines_pipeline_id_valves_update operation."""
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

        # Get valve data from arguments (or empty object if not provided)
        json_data = arguments.get("valves", {})

        response = await self.client.post(f"/api/v1/pipelines/{pipeline_id}/valves/update", json_data=json_data, params=params)

        self._log_execution_end(response)
        return response