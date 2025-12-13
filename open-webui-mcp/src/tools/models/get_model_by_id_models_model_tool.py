"""Get Model By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetModelByIdModelsModelTool(BaseTool):
    """Get Model By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_model_by_id_models_model",
            "description": "Get Model By Id",
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
        """Execute get_model_by_id_models_model operation."""
        self._log_execution_start(arguments)


        # Query parameter: id
        id = arguments.get("id")

        # Build request
        params = {}
        if id is not None:
            params["id"] = id

        response = await self.client.get("/api/v1/models/model", params=params)

        self._log_execution_end(response)
        return response