"""Ingredient management tools for batch and individual operations."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class IngredientsTool(BaseTool):
    """Manage recipe ingredients: batch create, read, update, delete."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_ingredients"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Manage recipe ingredients. "
            "Operations: 'batch_create' (multiple ingredients), 'get' (single ingredient), "
            "'update' (modify ingredient), 'delete' (remove ingredient)."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["batch_create", "get", "update", "delete"],
                    "description": "Operation to perform",
                },
                "recipe_id": {
                    "type": "string",
                    "description": "Recipe UUID (required for batch_create)",
                },
                "author_id": {
                    "type": "string",
                    "description": "Author UUID (required for batch_create)",
                },
                "ingredients": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "ingredient_name": {"type": "string"},
                            "ingredient_quantity": {"type": "string"},
                            "ingredient_measurement": {"type": "string"},
                        },
                    },
                    "description": "List of ingredients (required for batch_create)",
                },
                "ingredient_id": {
                    "type": "string",
                    "description": "Ingredient UUID (required for get, update, delete)",
                },
                "ingredient_name": {
                    "type": "string",
                    "description": "Ingredient name (required for update)",
                },
                "ingredient_quantity": {
                    "type": "string",
                    "description": "Ingredient quantity (required for update)",
                },
                "ingredient_measurement": {
                    "type": "string",
                    "description": "Ingredient measurement unit (required for update)",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ingredient operation.

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
                    "ingredients": params["ingredients"],
                }
                result = await self.http_client.post(
                    "/api/ingredient/create",
                    json=payload,
                )
            elif operation == "get":
                ingredient_id = params["ingredient_id"]
                result = await self.http_client.get(
                    f"/api/ingredient/{ingredient_id}"
                )
            elif operation == "update":
                ingredient_id = params["ingredient_id"]
                payload = {
                    "ingredient_name": params["ingredient_name"],
                    "ingredient_quantity": params["ingredient_quantity"],
                    "ingredient_measurement": params["ingredient_measurement"],
                }
                result = await self.http_client.put(
                    f"/api/ingredient/update/{ingredient_id}",
                    json=payload,
                )
            elif operation == "delete":
                ingredient_id = params["ingredient_id"]
                result = await self.http_client.delete(
                    f"/api/ingredient/delete/{ingredient_id}"
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
