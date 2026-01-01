"""Update Audio Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateAudioConfigAudioConfigUpdateTool(BaseTool):
    """Update Audio Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_audio_config_audio_config_update",
            "description": "Update Audio Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "tts": {
                        "type": "object",
                        "description": "TTS configuration settings",
                        "properties": {
                            "OPENAI_API_BASE_URL": {"type": "string"},
                            "OPENAI_API_KEY": {"type": "string"},
                            "API_KEY": {"type": "string"},
                            "ENGINE": {"type": "string"},
                            "MODEL": {"type": "string"},
                            "VOICE": {"type": "string"},
                            "SPLIT_ON": {"type": "string"},
                            "AZURE_SPEECH_REGION": {"type": "string"},
                            "AZURE_SPEECH_BASE_URL": {"type": "string"},
                            "AZURE_SPEECH_OUTPUT_FORMAT": {"type": "string"}
                        },
                        "required": ["OPENAI_API_BASE_URL", "OPENAI_API_KEY", "API_KEY", "ENGINE", "MODEL", "VOICE", "SPLIT_ON", "AZURE_SPEECH_REGION", "AZURE_SPEECH_BASE_URL", "AZURE_SPEECH_OUTPUT_FORMAT"]
                    },
                    "stt": {
                        "type": "object",
                        "description": "STT configuration settings",
                        "properties": {
                            "OPENAI_API_BASE_URL": {"type": "string"},
                            "OPENAI_API_KEY": {"type": "string"},
                            "ENGINE": {"type": "string"},
                            "MODEL": {"type": "string"},
                            "SUPPORTED_CONTENT_TYPES": {"type": "array", "items": {"type": "string"}},
                            "WHISPER_MODEL": {"type": "string"},
                            "DEEPGRAM_API_KEY": {"type": "string"},
                            "AZURE_API_KEY": {"type": "string"},
                            "AZURE_REGION": {"type": "string"},
                            "AZURE_LOCALES": {"type": "string"},
                            "AZURE_BASE_URL": {"type": "string"},
                            "AZURE_MAX_SPEAKERS": {"type": "string"}
                        },
                        "required": ["OPENAI_API_BASE_URL", "OPENAI_API_KEY", "ENGINE", "MODEL", "WHISPER_MODEL", "DEEPGRAM_API_KEY", "AZURE_API_KEY", "AZURE_REGION", "AZURE_LOCALES", "AZURE_BASE_URL", "AZURE_MAX_SPEAKERS"]
                    }
                },
                "required": ["tts", "stt"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_audio_config_audio_config_update operation."""
        self._log_execution_start(arguments)

        # Build request body per AudioConfigUpdateForm schema
        json_data = {
            "tts": arguments.get("tts"),
            "stt": arguments.get("stt")
        }

        response = await self.client.post("/api/v1/audio/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response