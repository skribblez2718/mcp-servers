"""Delete Tag By Id And Tag Name"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DeleteTagByIdAndTagNameChatsIdTagsTool(BaseTool):
    """Delete Tag By Id And Tag Name"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "delete_tag_by_id_and_tag_name_chats_id_tags",
            "description": "Delete Tag By Id And Tag Name",
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
        """Execute delete_tag_by_id_and_tag_name_chats_id_tags operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")


        # Build request
        params = {}

        response = await self.client.delete(f"/api/v1/chats/{id}/tags", params=params)

        self._log_execution_end(response)
        return response