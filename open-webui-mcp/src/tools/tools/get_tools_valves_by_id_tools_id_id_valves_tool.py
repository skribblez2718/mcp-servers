"""Get Tools Valves By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetToolsValvesByIdToolsIdIdValvesTool(BaseTool):
    """Get Tools Valves By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_tools_valves_by_id_tools_id_id_valves",
            "description": "Get Tools Valves By Id",
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
        """Execute get_tools_valves_by_id_tools_id_id_valves operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/v1/tools/id/{id}/valves", params=params)

        self._log_execution_end(response)
        return response