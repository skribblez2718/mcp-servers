"""Clone Shared Chat By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CloneSharedChatByIdChatsIdCloneSharedTool(BaseTool):
    """Clone Shared Chat By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "clone_shared_chat_by_id_chats_id_clone_shared",
            "description": "Clone Shared Chat By Id",
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
        """Execute clone_shared_chat_by_id_chats_id_clone_shared operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        json_data = {}

        response = await self.client.post(f"/api/v1/chats/{id}/clone/shared", json_data=json_data)

        self._log_execution_end(response)
        return response