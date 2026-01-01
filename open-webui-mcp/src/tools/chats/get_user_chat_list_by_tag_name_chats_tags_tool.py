"""Get User Chat List By Tag Name"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetUserChatListByTagNameChatsTagsTool(BaseTool):
    """Get User Chat List By Tag Name"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_user_chat_list_by_tag_name_chats_tags",
            "description": "Get User Chat List By Tag Name",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Tag name to filter chats by"
                    },
                    "skip": {
                        "type": ["integer", "null"],
                        "description": "Number of results to skip",
                        "default": 0
                    },
                    "limit": {
                        "type": ["integer", "null"],
                        "description": "Maximum number of results to return",
                        "default": 50
                    }
                },
                "required": ["name"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_user_chat_list_by_tag_name_chats_tags operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {"name": arguments["name"]}
        if arguments.get("skip") is not None:
            json_data["skip"] = arguments["skip"]
        if arguments.get("limit") is not None:
            json_data["limit"] = arguments["limit"]

        response = await self.client.post("/api/v1/chats/tags", json_data=json_data)

        self._log_execution_end(response)
        return response