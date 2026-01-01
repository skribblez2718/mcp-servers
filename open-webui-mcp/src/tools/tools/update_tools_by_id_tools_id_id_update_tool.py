"""Update Tools By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateToolsByIdToolsIdIdUpdateTool(BaseTool):
    """Update Tools By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_tools_by_id_tools_id_id_update",
            "description": "Update Tools By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The tool ID (path parameter)"
                    },
                    "tool_id": {
                        "type": "string",
                        "description": "The tool ID in the body (usually same as path id)"
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
                "required": ["id", "tool_id", "name", "content", "meta"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_tools_by_id_tools_id_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request - ToolForm body
        json_data = {
            "id": arguments.get("tool_id"),
            "name": arguments.get("name"),
            "content": arguments.get("content"),
            "meta": arguments.get("meta", {})
        }

        # Optional access_control
        if arguments.get("access_control") is not None:
            json_data["access_control"] = arguments.get("access_control")

        response = await self.client.post(f"/api/v1/tools/id/{id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response