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
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to generate an image from"
                    },
                    "model": {
                        "type": "string",
                        "description": "The model to use for generation (optional)"
                    },
                    "size": {
                        "type": "string",
                        "description": "The size of the generated image (optional, e.g. '1024x1024')"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of images to generate (optional, default: 1)"
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "Negative prompt to avoid certain elements (optional)"
                    }
                },
                "required": ["prompt"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute image_generations_images_generations operation."""
        self._log_execution_start(arguments)

        # Build request with required and optional fields
        json_data = {
            "prompt": arguments.get("prompt")
        }

        # Add optional fields if provided
        if arguments.get("model") is not None:
            json_data["model"] = arguments.get("model")
        if arguments.get("size") is not None:
            json_data["size"] = arguments.get("size")
        if arguments.get("n") is not None:
            json_data["n"] = arguments.get("n")
        if arguments.get("negative_prompt") is not None:
            json_data["negative_prompt"] = arguments.get("negative_prompt")

        response = await self.client.post("/api/v1/images/generations", json_data=json_data)

        self._log_execution_end(response)
        return response