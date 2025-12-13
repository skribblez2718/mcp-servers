"""Get Audio Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetAudioConfigAudioConfigTool(BaseTool):
    """Get Audio Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_audio_config_audio_config",
            "description": "Get Audio Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_audio_config_audio_config operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/audio/config", params=params)

        self._log_execution_end(response)
        return response