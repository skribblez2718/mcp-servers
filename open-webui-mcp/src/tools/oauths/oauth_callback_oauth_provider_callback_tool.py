"""Oauth Callback"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class OauthCallbackOauthProviderCallbackTool(BaseTool):
    """Oauth Callback"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "oauth_callback_oauth_provider_callback",
            "description": "Oauth Callback",
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
        """Execute oauth_callback_oauth_provider_callback operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: provider
        provider = arguments.get("provider")
        if provider:
            provider = ToolInputValidator.validate_id(provider, "provider")


        # Build request
        params = {}

        response = await self.client.get(f"/oauth/{provider}/callback", params=params)

        self._log_execution_end(response)
        return response