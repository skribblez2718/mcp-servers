"""Chat Action"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ChatActionChatActionsActionIdTool(BaseTool):
    """Chat Action"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "chat_action_chat_actions_action_id",
            "description": "Chat Action",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "action_id": {
                        "type": "string",
                        "description": ""
                    }
                },
                "required": ["action_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute chat_action_chat_actions_action_id operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: action_id
        action_id = arguments.get("action_id")
        if action_id:
            action_id = ToolInputValidator.validate_id(action_id, "action_id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/chat/actions/{action_id}", json_data=json_data)

        self._log_execution_end(response)
        return response