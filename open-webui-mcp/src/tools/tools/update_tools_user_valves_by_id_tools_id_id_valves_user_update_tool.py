"""Update Tools User Valves By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateToolsUserValvesByIdToolsIdIdValvesUserUpdateTool(BaseTool):
    """Update Tools User Valves By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_tools_user_valves_by_id_tools_id_id_valves_user_update",
            "description": "Update Tools User Valves By Id",
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
        """Execute update_tools_user_valves_by_id_tools_id_id_valves_user_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/tools/id/{id}/valves/user/update", json_data=json_data)

        self._log_execution_end(response)
        return response