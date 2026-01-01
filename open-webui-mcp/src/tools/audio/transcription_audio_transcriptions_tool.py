"""Transcription"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class TranscriptionAudioTranscriptionsTool(BaseTool):
    """Transcription - Transcribe audio file to text"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "transcription_audio_transcriptions",
            "description": "Transcribe audio file to text. Requires file path to audio file.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the audio file to transcribe"
                    },
                    "language": {
                        "type": "string",
                        "description": "Optional language code for transcription (e.g., 'en', 'es', 'fr')"
                    }
                },
                "required": ["file_path"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute transcription_audio_transcriptions operation."""
        self._log_execution_start(arguments)

        file_path = arguments.get("file_path")
        language = arguments.get("language")

        # Build additional form data for optional language parameter
        additional_data = {}
        if language is not None:
            additional_data["language"] = language

        # Use multipart/form-data upload per OpenAPI spec
        response = await self.client.post_with_file(
            "/api/v1/audio/transcriptions",
            file_path=file_path,
            field_name="file",
            additional_data=additional_data if additional_data else None
        )

        self._log_execution_end(response)
        return response