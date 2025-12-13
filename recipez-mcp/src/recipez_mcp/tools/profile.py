"""Profile management tools for user profile operations."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class ProfileGetTool(BaseTool):
    """Get current user profile information."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_profile_get"

    def description(self) -> str:
        """Return tool description."""
        return "Get the authenticated user's profile information."

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute profile get operation.

        Args:
            params: Empty dictionary (no parameters required)

        Returns:
            User profile data
        """
        start = time.time()

        try:
            result = await self.http_client.get("/api/profile/me")
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                "get_profile",
                duration,
                "success",
            )
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                "get_profile",
                duration,
                "error",
                error=str(e),
            )
            raise


class ProfileUpdateImageTool(BaseTool):
    """Update user profile image URL."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_profile_update_image"

    def description(self) -> str:
        """Return tool description."""
        return "Update the authenticated user's profile image URL."

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "URL to the new profile image",
                }
            },
            "required": ["image_url"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute profile image update operation.

        Args:
            params: Dictionary with 'image_url' key

        Returns:
            Success message
        """
        start = time.time()
        image_url = params["image_url"]

        try:
            result = await self.http_client.put(
                "/api/profile/image",
                json={"image_url": image_url},
            )
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                "update_image",
                duration,
                "success",
            )
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                "update_image",
                duration,
                "error",
                error=str(e),
            )
            raise
