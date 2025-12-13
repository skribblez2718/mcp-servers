"""Delete Model By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteModelByIdModelsModelTool(BaseTool):
    """Delete Model By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_model_by_id_models_model",
            "description": "Delete Model By Id",
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
        """Execute delete_model_by_id_models_model operation."""
        self._log_execution_start(arguments)


        # Query parameter: id
        id = arguments.get("id")

        # Build request
        params = {}
        if id is not None:
            params["id"] = id

        response = await self.client.delete("/api/v1/models/model/delete", params=params)

        self._log_execution_end(response)
        return response