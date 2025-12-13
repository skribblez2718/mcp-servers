"""Signup"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SignupAuthsSignupTool(BaseTool):
    """Signup"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "signup_auths_signup",
            "description": "Signup",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute signup_auths_signup operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/auths/signup", json_data=json_data)

        self._log_execution_end(response)
        return response