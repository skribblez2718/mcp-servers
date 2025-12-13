"""Chat get tool - Retrieve a specific chat by ID."""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ChatGetTool(BaseTool):
    """Retrieve a specific chat by ID.

    Returns complete chat details including messages.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition with schema
        """
        return {
            "name": "chat_get",
            "description": "Retrieve a specific chat by ID with all messages",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "Chat ID to retrieve"
                    }
                },
                "required": ["chat_id"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute chat retrieval.

        Args:
            arguments: Tool arguments with chat_id

        Returns:
            Chat details dict

        Raises:
            ValidationError: If chat_id invalid
            NotFoundError: If chat not found
            HTTPError: If API call fails
        """
        self._log_execution_start(arguments)

        # Extract and validate chat_id
        chat_id = arguments.get("chat_id")
        if not chat_id:
            from ...exceptions import ValidationError
            raise ValidationError("chat_id is required")

        chat_id = ToolInputValidator.validate_id(chat_id, "chat_id")

        # Call API
        response_data = await self.client.get(f"/api/v1/chats/{chat_id}")

        # Return response (API response is already in correct format)
        result = response_data

        self._log_execution_end(result)

        return result
