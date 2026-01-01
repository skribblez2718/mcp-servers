"""Create Folder"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateFolderFoldersTool(BaseTool):
    """Create Folder"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_folder_folders",
            "description": "Create Folder",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the folder"
                    },
                    "data": {
                        "type": "object",
                        "description": "Optional additional data for the folder",
                        "additionalProperties": True
                    }
                },
                "required": ["name"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_folder_folders operation."""
        self._log_execution_start(arguments)

        # Build request with FolderForm schema
        json_data = {
            "name": arguments.get("name")
        }
        if arguments.get("data"):
            json_data["data"] = arguments.get("data")

        response = await self.client.post("/api/v1/folders/", json_data=json_data)

        self._log_execution_end(response)
        return response