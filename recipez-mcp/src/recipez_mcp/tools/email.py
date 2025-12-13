"""Email tools for invitations and recipe sharing."""

import time
from typing import Any, Dict, List

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class EmailTool(BaseTool):
    """Send emails: invitations, recipe link sharing, full recipe sharing."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_email"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Send emails through Recipez. "
            "Operations: 'invite' (invitation to join), "
            "'share_link' (share recipe link), "
            "'share_full' (share complete recipe content with ingredients and steps)."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["invite", "share_link", "share_full"],
                    "description": "Email operation to perform",
                },
                "email": {
                    "type": "string",
                    "description": "Recipient email address (required for all operations)",
                },
                "sender_name": {
                    "type": "string",
                    "description": "Name of sender (required for all operations)",
                },
                "invite_link": {
                    "type": "string",
                    "description": "Invitation link URL (required for invite)",
                },
                "recipe_name": {
                    "type": "string",
                    "description": "Recipe name (required for share_link and share_full)",
                },
                "recipe_link": {
                    "type": "string",
                    "description": "Recipe link URL (required for share_link)",
                },
                "recipe_description": {
                    "type": "string",
                    "description": "Recipe description (optional for share_full)",
                },
                "recipe_ingredients": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Recipe ingredients list (required for share_full)",
                },
                "recipe_steps": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Recipe steps list (required for share_full)",
                },
            },
            "required": ["operation", "email", "sender_name"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email operation.

        Args:
            params: Dictionary with operation and operation-specific parameters

        Returns:
            Success message
        """
        start = time.time()
        operation = params["operation"]

        try:
            if operation == "invite":
                payload = {
                    "email": params["email"],
                    "invite_link": params["invite_link"],
                    "sender_name": params["sender_name"],
                }
                result = await self.http_client.post(
                    "/api/email/invite",
                    json=payload,
                )
            elif operation == "share_link":
                payload = {
                    "email": params["email"],
                    "recipe_name": params["recipe_name"],
                    "recipe_link": params["recipe_link"],
                    "sender_name": params["sender_name"],
                }
                result = await self.http_client.post(
                    "/api/email/recipe-share",
                    json=payload,
                )
            elif operation == "share_full":
                payload = {
                    "email": params["email"],
                    "recipe_name": params["recipe_name"],
                    "recipe_ingredients": params["recipe_ingredients"],
                    "recipe_steps": params["recipe_steps"],
                    "sender_name": params["sender_name"],
                }
                if "recipe_description" in params:
                    payload["recipe_description"] = params["recipe_description"]

                result = await self.http_client.post(
                    "/api/email/recipe-share-full",
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
