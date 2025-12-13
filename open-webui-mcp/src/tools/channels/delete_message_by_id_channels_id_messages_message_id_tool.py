"""Delete Message By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteMessageByIdChannelsIdMessagesMessageIdTool(BaseTool):
    """Delete Message By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_message_by_id_channels_id_messages_message_id",
            "description": "Delete Message By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    },
                    "message_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["id", "message_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute delete_message_by_id_channels_id_messages_message_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")
        # Validate path parameter: message_id
        message_id = arguments.get("message_id")
        if message_id:
            message_id = ToolInputValidator.validate_id(message_id, "message_id")


        # Build request
        params = {}

        response = await self.client.delete(f"/api/v1/channels/{id}/messages/{message_id}/delete", params=params)

        self._log_execution_end(response)
        return response