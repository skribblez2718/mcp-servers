"""Remove Users From Group"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class RemoveUsersFromGroupGroupsIdIdUsersRemoveTool(BaseTool):
    """Remove Users From Group"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "remove_users_from_group_groups_id_id_users_remove",
            "description": "Remove Users From Group",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The group ID to remove users from"
                    },
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of user IDs to remove from the group"
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute remove_users_from_group_groups_id_id_users_remove operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request with UserIdsForm schema
        json_data = {}
        if arguments.get("user_ids"):
            json_data["user_ids"] = arguments.get("user_ids")

        response = await self.client.post(f"/api/v1/groups/id/{id}/users/remove", json_data=json_data)

        self._log_execution_end(response)
        return response