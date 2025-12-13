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
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_webhook_url_webhook operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/webhook", json_data=json_data)

        self._log_execution_end(response)
        return response