"""Get Channel Thread Messages"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetChannelThreadMessagesChannelsIdMessagesMessageIdThreadTool(BaseTool):
    """Get Channel Thread Messages"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_channel_thread_messages_channels_id_messages_message_id_thread",
            "description": "Get Channel Thread Messages",
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
                    },
                    "skip": {
                        "type": "integer",
                        "description": "",
                        "default": 0
                    },
                    "limit": {
                        "type": "integer",
                        "description": "",
                        "default": 50
                    }
                },
                "required": ["id", "message_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_channel_thread_messages_channels_id_messages_message_id_thread operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")
        # Validate path parameter: message_id
        message_id = arguments.get("message_id")
        if message_id:
            message_id = ToolInputValidator.validate_id(message_id, "message_id")

        # Query parameter: skip
        skip = arguments.get("skip", 0)
        # Query parameter: limit
        limit = arguments.get("limit", 50)

        # Build request
        params = {}
        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit

        response = await self.client.get(f"/api/v1/channels/{id}/messages/{message_id}/thread", params=params)

        self._log_execution_end(response)
        return response