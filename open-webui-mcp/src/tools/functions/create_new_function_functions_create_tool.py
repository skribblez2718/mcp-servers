"""Create New Function"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewFunctionFunctionsCreateTool(BaseTool):
    """Create New Function"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_function_functions_create",
            "description": "Create New Function",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The function ID"
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
                "required": ["id", "name", "content", "meta"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_function_functions_create operation."""
        self._log_execution_start(arguments)

        # Build request with FunctionForm schema
        json_data = {
            "id": arguments.get("id"),
            "name": arguments.get("name"),
            "content": arguments.get("content"),
            "meta": arguments.get("meta", {})
        }

        response = await self.client.post("/api/v1/functions/create", json_data=json_data)

        self._log_execution_end(response)
        return response