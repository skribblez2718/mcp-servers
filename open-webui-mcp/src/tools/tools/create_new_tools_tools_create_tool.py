"""Create New Tools"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewToolsToolsCreateTool(BaseTool):
    """Create New Tools"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_tools_tools_create",
            "description": "Create New Tools",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The tool ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "The tool name"
                    },
                    "content": {
                        "type": "string",
                        "description": "The tool content/code"
                    },
                    "meta": {
                        "type": "object",
                        "description": "Tool metadata with optional description and manifest",
                        "properties": {
                            "description": {
                                "type": ["string", "null"],
                                "description": "Tool description"
                            },
                            "manifest": {
                                "type": ["object", "null"],
                                "additionalProperties": True,
                                "description": "Tool manifest"
                            }
                        }
                    },
                    "access_control": {
                        "type": ["object", "null"],
                        "additionalProperties": True,
                        "description": "Optional access control settings"
                    }
                },
                "required": ["id", "name", "content", "meta"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_tools_tools_create operation."""
        self._log_execution_start(arguments)

        # Build request - ToolForm
        json_data = {
            "id": arguments.get("id"),
            "name": arguments.get("name"),
            "content": arguments.get("content"),
            "meta": arguments.get("meta", {})
        }

        # Optional access_control
        if arguments.get("access_control") is not None:
            json_data["access_control"] = arguments.get("access_control")

        response = await self.client.post("/api/v1/tools/create", json_data=json_data)

        self._log_execution_end(response)
        return response