"""Send Chat Message Event By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SendChatMessageEventByIdChatsIdMessagesMessageIdEventTool(BaseTool):
    """Send Chat Message Event By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "send_chat_message_event_by_id_chats_id_messages_message_id_event",
            "description": "Send Chat Message Event By Id",
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
        """Execute send_chat_message_event_by_id_chats_id_messages_message_id_event operation."""
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
        json_data = {}

        response = await self.client.post(f"/api/v1/chats/{id}/messages/{message_id}/event", json_data=json_data)

        self._log_execution_end(response)
        return response