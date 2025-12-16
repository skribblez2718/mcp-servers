"""AI-powered tools for recipe generation and modification."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class AITool(BaseTool):
    """AI-powered recipe operations: create and modify."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_ai"

    def description(self) -> str:
        """Return tool description."""
        return (
            "AI-powered recipe operations. "
            "Operations: 'create' (generate recipe from prompt), "
            "'modify' (modify existing recipe with instructions)."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["create", "modify"],
                    "description": "AI operation to perform",
                },
                "message": {
                    "type": "string",
                    "description": "Prompt or instructions (required for create and modify)",
                },
                "recipe_id": {
                    "type": "string",
                    "description": "Recipe UUID (required for modify)",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI operation.

        Args:
            params: Dictionary with operation and operation-specific parameters

        Returns:
            Operation result
        """
        start = time.time()
        operation = params["operation"]

        try:
            if operation == "create":
                payload = {"message": params["message"]}
                result = await self.http_client.post(
                    "/api/ai/create",
                    json=payload,
                )
            elif operation == "modify":
                payload = {
                    "message": params["message"],
                    "recipe_id": params["recipe_id"],
                }
                result = await self.http_client.post(
                    "/api/ai/modify",
                    json=payload,
                )
            else:
                raise ValueError(f"Invalid operation: {operation}")

            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                operation,
                duration,
                "success",
            )
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                operation,
                duration,
                "error",
                error=str(e),
            )
            raise
