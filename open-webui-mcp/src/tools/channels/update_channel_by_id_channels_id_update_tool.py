"""Update Channel By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateChannelByIdChannelsIdUpdateTool(BaseTool):
    """Update Channel By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_channel_by_id_channels_id_update",
            "description": "Update Channel By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Channel ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Channel name"
                    },
                    "description": {
                        "type": ["string", "null"],
                        "description": "Channel description"
                    },
                    "data": {
                        "type": ["object", "null"],
                        "description": "Additional channel data",
                        "additionalProperties": True
                    },
                    "meta": {
                        "type": ["object", "null"],
                        "description": "Channel metadata",
                        "additionalProperties": True
                    },
                    "access_control": {
                        "type": ["object", "null"],
                        "description": "Access control settings",
                        "additionalProperties": True
                    }
                },
                "required": ["id", "name"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_channel_by_id_channels_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {
            "name": arguments.get("name")
        }
        # Add optional fields if provided
        if arguments.get("description") is not None:
            json_data["description"] = arguments.get("description")
        if arguments.get("data") is not None:
            json_data["data"] = arguments.get("data")
        if arguments.get("meta") is not None:
            json_data["meta"] = arguments.get("meta")
        if arguments.get("access_control") is not None:
            json_data["access_control"] = arguments.get("access_control")

        response = await self.client.post(f"/api/v1/channels/{id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response