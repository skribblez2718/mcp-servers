"""Image Generations"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ImageGenerationsImagesGenerationsTool(BaseTool):
    """Image Generations"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "image_generations_images_generations",
            "description": "Image Generations",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute image_generations_images_generations operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/images/generations", json_data=json_data)

        self._log_execution_end(response)
        return response