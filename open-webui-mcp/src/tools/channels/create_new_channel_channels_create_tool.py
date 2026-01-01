"""Create New Channel"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewChannelChannelsCreateTool(BaseTool):
    """Create New Channel"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_channel_channels_create",
            "description": "Create New Channel",
            "inputSchema": {
                "type": "object",
                "properties": {
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
                "required": ["name"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_channel_channels_create operation."""
        self._log_execution_start(arguments)



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

        response = await self.client.post("/api/v1/channels/create", json_data=json_data)

        self._log_execution_end(response)
        return response