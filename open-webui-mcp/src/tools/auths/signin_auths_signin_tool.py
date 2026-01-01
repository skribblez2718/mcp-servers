"""Signin"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SigninAuthsSigninTool(BaseTool):
    """Signin"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "signin_auths_signin",
            "description": "Signin",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    },
                    "password": {
                        "type": "string",
                        "description": "User password"
                    }
                },
                "required": ["email", "password"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute signin_auths_signin operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "email": arguments.get("email"),
            "password": arguments.get("password")
        }

        response = await self.client.post("/api/v1/auths/signin", json_data=json_data)

        self._log_execution_end(response)
        return response