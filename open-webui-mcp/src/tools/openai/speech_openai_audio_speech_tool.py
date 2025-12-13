"""Speech"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SpeechOpenaiAudioSpeechTool(BaseTool):
    """Speech"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "speech_openai_audio_speech",
            "description": "Speech",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute speech_openai_audio_speech operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/openai/audio/speech", json_data=json_data)

        self._log_execution_end(response)
        return response