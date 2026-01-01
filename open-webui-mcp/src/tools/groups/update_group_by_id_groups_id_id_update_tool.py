"""Update Group By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateGroupByIdGroupsIdIdUpdateTool(BaseTool):
    """Update Group By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_group_by_id_groups_id_id_update",
            "description": "Update Group By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The group ID to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "The new name for the group"
                    },
                    "description": {
                        "type": "string",
                        "description": "The new description for the group"
                    },
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of user IDs in the group"
                    },
                    "permissions": {
                        "type": "object",
                        "description": "Optional permissions configuration",
                        "additionalProperties": True
                    }
                },
                "required": ["id", "name", "description"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_group_by_id_groups_id_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request with GroupUpdateForm schema
        json_data = {
            "name": arguments.get("name"),
            "description": arguments.get("description")
        }
        if arguments.get("user_ids"):
            json_data["user_ids"] = arguments.get("user_ids")
        if arguments.get("permissions"):
            json_data["permissions"] = arguments.get("permissions")

        response = await self.client.post(f"/api/v1/groups/id/{id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response