"""Image management tools for upload and deletion."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class ImagesTool(BaseTool):
    """Manage recipe images: upload base64-encoded images and delete."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_images"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Manage recipe images. "
            "Operations: 'upload' (base64-encoded image data), 'delete' (remove image). "
            "Maximum upload size: 10MB."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["upload", "delete"],
                    "description": "Operation to perform",
                },
                "image_data": {
                    "type": "string",
                    "description": "Base64-encoded image data (required for upload)",
                },
                "image_path": {
                    "type": "string",
                    "description": "File path where image will be stored (required for upload)",
                },
                "author_id": {
                    "type": "string",
                    "description": "Author UUID (required for upload)",
                },
                "image_id": {
                    "type": "string",
                    "description": "Image UUID (required for delete)",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute image operation.

        Args:
            params: Dictionary with operation and operation-specific parameters

        Returns:
            Operation result
        """
        start = time.time()
        operation = params["operation"]

        try:
            if operation == "upload":
                payload = {
                    "image_data": params["image_data"],
                    "image_path": params["image_path"],
                    "author_id": params["author_id"],
                }
                result = await self.http_client.post(
                    "/api/image/create",
                    json=payload,
                )
            elif operation == "delete":
                image_id = params["image_id"]
                result = await self.http_client.delete(
                    f"/api/image/delete/{image_id}"
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
