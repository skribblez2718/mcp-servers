"""Oauth Login"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class OauthLoginOauthProviderLoginTool(BaseTool):
    """Oauth Login"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "oauth_login_oauth_provider_login",
            "description": "Oauth Login",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "provider": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["provider"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute oauth_login_oauth_provider_login operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: provider
        provider = arguments.get("provider")
        if provider:
            provider = ToolInputValidator.validate_id(provider, "provider")


        # Build request
        params = {}

        response = await self.client.get(f"/oauth/{provider}/login", params=params)

        self._log_execution_end(response)
        return response