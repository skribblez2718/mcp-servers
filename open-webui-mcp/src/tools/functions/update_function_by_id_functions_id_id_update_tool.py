"""Update Function By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateFunctionByIdFunctionsIdIdUpdateTool(BaseTool):
    """Update Function By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_function_by_id_functions_id_id_update",
            "description": "Update Function By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The function ID (path parameter)"
                    },
                    "function_id": {
                        "type": "string",
                        "description": "The function ID in the body (usually same as path id)"
                    },
                    "name": {
                        "type": "string",
                        "description": "The function name"
                    },
                    "content": {
                        "type": "string",
                        "description": "The function content/code"
                    },
                    "meta": {
                        "type": "object",
                        "description": "Function metadata with optional description and manifest",
                        "properties": {
                            "description": {
                                "type": ["string", "null"],
                                "description": "Function description"
                            },
                            "manifest": {
                                "type": ["object", "null"],
                                "additionalProperties": True,
                                "description": "Function manifest"
                            }
                        }
                    }
                },
                "required": ["id", "function_id", "name", "content", "meta"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_function_by_id_functions_id_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

        # Build request with FunctionForm schema
        json_data = {
            "id": arguments.get("function_id"),
            "name": arguments.get("name"),
            "content": arguments.get("content"),
            "meta": arguments.get("meta", {})
        }

        response = await self.client.post(f"/api/v1/functions/id/{id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response