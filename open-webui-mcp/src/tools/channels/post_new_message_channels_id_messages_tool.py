"""Post New Message"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class PostNewMessageChannelsIdMessagesTool(BaseTool):
    """Post New Message"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "post_new_message_channels_id_messages",
            "description": "Post New Message",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute post_new_message_channels_id_messages operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/channels/{id}/messages/post", json_data=json_data)

        self._log_execution_end(response)
        return response