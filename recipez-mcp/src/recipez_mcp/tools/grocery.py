"""Grocery list tool for AI-organized shopping lists from recipes."""

import time
from typing import Any, Dict, List

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class GroceryTool(BaseTool):
    """Generate AI-organized grocery list from recipe selections."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_grocery"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Generate an AI-organized grocery list from selected recipes. "
            "Consolidates ingredients, organizes by store department, and emails to user. "
            "Maximum 50 recipes per request."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "recipe_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of recipe UUIDs (1-50 recipes)",
                    "minItems": 1,
                    "maxItems": 50,
                },
            },
            "required": ["recipe_ids"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute grocery list generation.

        Args:
            params: Dictionary with 'recipe_ids' list

        Returns:
            Success message confirming email sent
        """
        start = time.time()
        recipe_ids: List[str] = params["recipe_ids"]

        # Validate recipe count
        if len(recipe_ids) < 1 or len(recipe_ids) > 50:
            raise ValueError(
                f"Recipe count must be between 1 and 50, got {len(recipe_ids)}"
            )

        try:
            payload = {"recipe_ids": recipe_ids}
            result = await self.http_client.post(
                "/api/grocery/send",
                json=payload,
            )

            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                f"send_grocery_list_{len(recipe_ids)}_recipes",
                duration,
                "success",
            )
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                f"send_grocery_list_{len(recipe_ids)}_recipes",
                duration,
                "error",
                error=str(e),
            )
            raise
