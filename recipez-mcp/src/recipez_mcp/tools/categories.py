"""Category management tools for CRUD operations."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class CategoriesTool(BaseTool):
    """Manage recipe categories: create, read, list, update, delete, preview deletion."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_categories"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Manage recipe categories with full CRUD operations. "
            "Operations: 'create' (new category), 'get' (single category), "
            "'list' (all categories), 'update' (modify category), "
            "'delete' (remove category), 'preview_delete' (check impact before deletion)."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["create", "get", "list", "update", "delete", "preview_delete"],
                    "description": "Operation to perform",
                },
                "category_id": {
                    "type": "string",
                    "description": "Category UUID (required for get, update, delete, preview_delete)",
                },
                "category_name": {
                    "type": "string",
                    "description": "Category name (required for create and update)",
                },
                "author_id": {
                    "type": "string",
                    "description": "Author UUID (required for create)",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute category operation.

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
                    "category_name": params["category_name"],
                    "author_id": params["author_id"],
                }
                result = await self.http_client.post(
                    "/api/category/create",
                    json=payload,
                )
            elif operation == "get":
                category_id = params["category_id"]
                result = await self.http_client.get(f"/api/category/{category_id}")
            elif operation == "list":
                result = await self.http_client.get("/api/category/all")
            elif operation == "update":
                category_id = params["category_id"]
                payload = {"category_name": params["category_name"]}
                result = await self.http_client.put(
                    f"/api/category/update/{category_id}",
                    json=payload,
                )
            elif operation == "delete":
                category_id = params["category_id"]
                result = await self.http_client.delete(
                    f"/api/category/delete/{category_id}"
                )
            elif operation == "preview_delete":
                category_id = params["category_id"]
                result = await self.http_client.get(
                    f"/api/category/delete/{category_id}/preview"
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
