"""Step management tools for batch and individual operations."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class StepsTool(BaseTool):
    """Manage recipe steps: batch create, read by recipe, update, delete."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_steps"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Manage recipe steps/instructions. "
            "Operations: 'batch_create' (multiple steps), 'get_by_recipe' (all steps for recipe), "
            "'update' (modify step), 'delete' (remove step)."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["batch_create", "get_by_recipe", "update", "delete"],
                    "description": "Operation to perform",
                },
                "recipe_id": {
                    "type": "string",
                    "description": "Recipe UUID (required for batch_create and get_by_recipe)",
                },
                "author_id": {
                    "type": "string",
                    "description": "Author UUID (required for batch_create)",
                },
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step_description": {"type": "string"},
                        },
                    },
                    "description": "List of steps (required for batch_create)",
                },
                "step_id": {
                    "type": "string",
                    "description": "Step UUID (required for update, delete)",
                },
                "step_description": {
                    "type": "string",
                    "description": "Step description text (required for update)",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute step operation.

        Args:
            params: Dictionary with operation and operation-specific parameters

        Returns:
            Operation result
        """
        start = time.time()
        operation = params["operation"]

        try:
            if operation == "batch_create":
                payload = {
                    "recipe_id": params["recipe_id"],
                    "author_id": params["author_id"],
                    "steps": params["steps"],
                }
                result = await self.http_client.post(
                    "/api/step/create",
                    json=payload,
                )
            elif operation == "get_by_recipe":
                recipe_id = params["recipe_id"]
                result = await self.http_client.get(f"/api/step/{recipe_id}")
            elif operation == "update":
                step_id = params["step_id"]
                payload = {"step_description": params["step_description"]}
                result = await self.http_client.put(
                    f"/api/step/update/{step_id}",
                    json=payload,
                )
            elif operation == "delete":
                step_id = params["step_id"]
                result = await self.http_client.delete(
                    f"/api/step/delete/{step_id}"
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
