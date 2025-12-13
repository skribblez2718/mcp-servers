"""Add User To Group"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class AddUserToGroupGroupsIdIdUsersAddTool(BaseTool):
    """Add User To Group"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "add_user_to_group_groups_id_id_users_add",
            "description": "Add User To Group",
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
        """Execute add_user_to_group_groups_id_id_users_add operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/groups/id/{id}/users/add", json_data=json_data)

        self._log_execution_end(response)
        return response