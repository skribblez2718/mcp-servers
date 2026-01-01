"""Set Banners"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetBannersConfigsBannersTool(BaseTool):
    """Set Banners"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_banners_configs_banners",
            "description": "Set Banners",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "banners": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "description": "Banner ID"},
                                "type": {"type": "string", "description": "Banner type (e.g., 'info', 'warning', 'error')"},
                                "title": {"type": ["string", "null"], "description": "Banner title (optional)"},
                                "content": {"type": "string", "description": "Banner content"},
                                "dismissible": {"type": "boolean", "description": "Whether banner can be dismissed"},
                                "timestamp": {"type": "integer", "description": "Unix timestamp for the banner"}
                            },
                            "required": ["id", "type", "content", "dismissible", "timestamp"]
                        },
                        "description": "Array of banner configurations"
                    }
                },
                "required": ["banners"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_banners_configs_banners operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {
            "banners": arguments.get("banners", [])
        }

        response = await self.client.post("/api/v1/configs/banners", json_data=json_data)

        self._log_execution_end(response)
        return response