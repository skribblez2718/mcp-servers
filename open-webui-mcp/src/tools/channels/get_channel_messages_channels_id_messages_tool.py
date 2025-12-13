"""Get Channel Messages"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetChannelMessagesChannelsIdMessagesTool(BaseTool):
    """Get Channel Messages"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_channel_messages_channels_id_messages",
            "description": "Get Channel Messages",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
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
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_channel_messages_channels_id_messages operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

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

        response = await self.client.get(f"/api/v1/channels/{id}/messages", params=params)

        self._log_execution_end(response)
        return response