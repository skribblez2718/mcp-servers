"""Update Webhook Url"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateWebhookUrlWebhookTool(BaseTool):
    """Update Webhook Url"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_webhook_url_webhook",
            "description": "Update Webhook Url",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The webhook URL to set"
                    }
                },
                "required": ["url"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_webhook_url_webhook operation."""
        self._log_execution_start(arguments)

        # Build request with UrlForm
        json_data = {
            "url": arguments.get("url")
        }

        response = await self.client.post("/api/webhook", json_data=json_data)

        self._log_execution_end(response)
        return response