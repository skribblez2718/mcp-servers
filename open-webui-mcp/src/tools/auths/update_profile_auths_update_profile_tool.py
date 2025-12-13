"""Update Profile"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateProfileAuthsUpdateProfileTool(BaseTool):
    """Update Profile"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_profile_auths_update_profile",
            "description": "Update Profile",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_profile_auths_update_profile operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/auths/update/profile", json_data=json_data)

        self._log_execution_end(response)
        return response