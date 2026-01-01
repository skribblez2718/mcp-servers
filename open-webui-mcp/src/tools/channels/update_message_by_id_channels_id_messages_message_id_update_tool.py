"""Update Message By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateMessageByIdChannelsIdMessagesMessageIdUpdateTool(BaseTool):
    """Update Message By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_message_by_id_channels_id_messages_message_id_update",
            "description": "Update Message By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Channel ID"
                    },
                    "message_id": {
                        "type": "string",
                        "description": "Message ID"
                    },
                    "content": {
                        "type": "string",
                        "description": "Message content"
                    },
                    "parent_id": {
                        "type": ["string", "null"],
                        "description": "Parent message ID for threaded replies"
                    },
                    "data": {
                        "type": ["object", "null"],
                        "description": "Additional message data",
                        "additionalProperties": True
                    },
                    "meta": {
                        "type": ["object", "null"],
                        "description": "Message metadata",
                        "additionalProperties": True
                    }
                },
                "required": ["id", "message_id", "content"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_message_by_id_channels_id_messages_message_id_update operation."""
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
        json_data = {
            "content": arguments.get("content")
        }
        # Add optional fields if provided
        if arguments.get("parent_id") is not None:
            json_data["parent_id"] = arguments.get("parent_id")
        if arguments.get("data") is not None:
            json_data["data"] = arguments.get("data")
        if arguments.get("meta") is not None:
            json_data["meta"] = arguments.get("meta")

        response = await self.client.post(f"/api/v1/channels/{id}/messages/{message_id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response