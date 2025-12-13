"""Recipe management tools for CRUD operations."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class RecipesTool(BaseTool):
    """Manage recipes: create, read, list, update, delete, and batch operations."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_recipes"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Manage recipes with full CRUD operations. "
            "Operations: 'create' (new recipe), 'get' (single recipe), "
            "'list' (all recipes), 'update' (modify recipe), "
            "'delete' (remove recipe), 'batch_update_category' (bulk category update)."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["create", "get", "list", "update", "delete", "batch_update_category"],
                    "description": "Operation to perform",
                },
                "recipe_id": {
                    "type": "string",
                    "description": "Recipe UUID (required for get, update, delete)",
                },
                "recipe_name": {
                    "type": "string",
                    "description": "Recipe name (required for create, optional for update)",
                },
                "recipe_description": {
                    "type": "string",
                    "description": "Recipe description (required for create, optional for update)",
                },
                "recipe_category_id": {
                    "type": "string",
                    "description": "Category UUID (required for create, optional for update)",
                },
                "recipe_image_id": {
                    "type": "string",
                    "description": "Image UUID (required for create, optional for update)",
                },
                "recipe_author_id": {
                    "type": "string",
                    "description": "Author UUID (required for create)",
                },
                "updates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "recipe_id": {"type": "string"},
                            "category_id": {"type": "string"},
                        },
                    },
                    "description": "Batch updates for batch_update_category",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute recipe operation.

        Args:
            params: Dictionary with operation and operation-specific parameters

        Returns:
            Operation result
        """
        start = time.time()
        operation = params["operation"]

        try:
            if operation == "create":
                payload = {
                    "recipe_name": params["recipe_name"],
                    "recipe_description": params["recipe_description"],
                    "recipe_category_id": params["recipe_category_id"],
                    "recipe_image_id": params["recipe_image_id"],
                    "recipe_author_id": params["recipe_author_id"],
                }
                result = await self.http_client.post(
                    "/api/recipe/create",
                    json=payload,
                )
            elif operation == "get":
                recipe_id = params["recipe_id"]
                result = await self.http_client.get(f"/api/recipe/{recipe_id}")
            elif operation == "list":
                result = await self.http_client.get("/api/recipe/all")
            elif operation == "update":
                recipe_id = params["recipe_id"]
                payload = {}
                if "recipe_name" in params:
                    payload["recipe_name"] = params["recipe_name"]
                if "recipe_description" in params:
                    payload["recipe_description"] = params["recipe_description"]
                if "recipe_category_id" in params:
                    payload["recipe_category_id"] = params["recipe_category_id"]
                if "recipe_image_id" in params:
                    payload["recipe_image_id"] = params["recipe_image_id"]

                result = await self.http_client.put(
                    f"/api/recipe/update/{recipe_id}",
                    json=payload,
                )
            elif operation == "delete":
                recipe_id = params["recipe_id"]
                result = await self.http_client.delete(
                    f"/api/recipe/delete/{recipe_id}"
                )
            elif operation == "batch_update_category":
                result = await self.http_client.post(
                    "/api/recipe/batch-update-category",
                    json={"updates": params["updates"]},
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
