"""Update Tools Valves By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateToolsValvesByIdToolsIdIdValvesUpdateTool(BaseTool):
    """Update Tools Valves By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_tools_valves_by_id_tools_id_id_valves_update",
            "description": "Update Tools Valves By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The tool ID (path parameter)"
                    },
                    "valves": {
                        "type": "object",
                        "additionalProperties": True,
                        "description": "The valve configuration data to update"
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_tools_valves_by_id_tools_id_id_valves_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request - generic object body
        # If valves object provided, use it; otherwise use remaining arguments
        json_data = arguments.get("valves", {})
        if not json_data:
            json_data = {k: v for k, v in arguments.items() if k != "id"}

        response = await self.client.post(f"/api/v1/tools/id/{id}/valves/update", json_data=json_data)

        self._log_execution_end(response)
        return response