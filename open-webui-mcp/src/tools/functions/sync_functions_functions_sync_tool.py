"""Sync Functions"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SyncFunctionsFunctionsSyncTool(BaseTool):
    """Sync Functions"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "sync_functions_functions_sync",
            "description": "Sync Functions",
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
                    },
                    "functions": {
                        "type": "array",
                        "description": "Optional array of FunctionModel objects to sync",
                        "items": {
                            "type": "object",
                            "additionalProperties": True
                        }
                    }
                },
                "required": ["id", "name", "content", "meta"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute sync_functions_functions_sync operation."""
        self._log_execution_start(arguments)

        # Build request with SyncFunctionsForm schema
        json_data = {
            "id": arguments.get("id"),
            "name": arguments.get("name"),
            "content": arguments.get("content"),
            "meta": arguments.get("meta", {})
        }
        if arguments.get("functions") is not None:
            json_data["functions"] = arguments.get("functions")

        response = await self.client.post("/api/v1/functions/sync", json_data=json_data)

        self._log_execution_end(response)
        return response