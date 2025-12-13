"""Update Model By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateModelByIdModelsModelUpdateTool(BaseTool):
    """Update Model By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_model_by_id_models_model_update",
            "description": "Update Model By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_model_by_id_models_model_update operation."""
        self._log_execution_start(arguments)


        # Query parameter: id
        id = arguments.get("id")

        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/models/model/update", json_data=json_data)

        self._log_execution_end(response)
        return response