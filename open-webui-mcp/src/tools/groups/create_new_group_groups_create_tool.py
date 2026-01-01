"""Create New Group"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewGroupGroupsCreateTool(BaseTool):
    """Create New Group"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_group_groups_create",
            "description": "Create New Group",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the group"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the group"
                    },
                    "permissions": {
                        "type": "object",
                        "description": "Optional permissions configuration",
                        "additionalProperties": True
                    }
                },
                "required": ["name", "description"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_group_groups_create operation."""
        self._log_execution_start(arguments)

        # Build request with GroupForm schema
        json_data = {
            "name": arguments.get("name"),
            "description": arguments.get("description")
        }
        if arguments.get("permissions"):
            json_data["permissions"] = arguments.get("permissions")

        response = await self.client.post("/api/v1/groups/create", json_data=json_data)

        self._log_execution_end(response)
        return response