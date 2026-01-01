"""Update Image Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateImageConfigImagesImageConfigUpdateTool(BaseTool):
    """Update Image Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_image_config_images_image_config_update",
            "description": "Update Image Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "MODEL": {
                        "type": "string",
                        "description": "The default image generation model"
                    },
                    "IMAGE_SIZE": {
                        "type": "string",
                        "description": "Default image size (e.g. '512x512', '1024x1024')"
                    },
                    "IMAGE_STEPS": {
                        "type": "integer",
                        "description": "Number of steps for image generation"
                    }
                },
                "required": ["MODEL", "IMAGE_SIZE", "IMAGE_STEPS"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_image_config_images_image_config_update operation."""
        self._log_execution_start(arguments)

        # Build request with ImageConfigForm fields
        json_data = {
            "MODEL": arguments.get("MODEL"),
            "IMAGE_SIZE": arguments.get("IMAGE_SIZE"),
            "IMAGE_STEPS": arguments.get("IMAGE_STEPS")
        }

        response = await self.client.post("/api/v1/images/image/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response