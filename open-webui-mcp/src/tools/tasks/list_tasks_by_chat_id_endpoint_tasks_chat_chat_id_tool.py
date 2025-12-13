"""List Tasks By Chat Id Endpoint"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ListTasksByChatIdEndpointTasksChatChatIdTool(BaseTool):
    """List Tasks By Chat Id Endpoint"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "list_tasks_by_chat_id_endpoint_tasks_chat_chat_id",
            "description": "List Tasks By Chat Id Endpoint",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["chat_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute list_tasks_by_chat_id_endpoint_tasks_chat_chat_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: chat_id
        chat_id = arguments.get("chat_id")
        if chat_id:
            chat_id = ToolInputValidator.validate_id(chat_id, "chat_id")


        # Build request
        params = {}

        response = await self.client.get(f"/api/tasks/chat/{chat_id}", params=params)

        self._log_execution_end(response)
        return response