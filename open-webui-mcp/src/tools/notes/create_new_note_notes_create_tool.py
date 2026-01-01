"""Create New Note"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewNoteNotesCreateTool(BaseTool):
    """Create New Note"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_note_notes_create",
            "description": "Create New Note",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the note"
                    },
                    "data": {
                        "type": "object",
                        "description": "Optional note content/data",
                        "additionalProperties": True
                    },
                    "meta": {
                        "type": "object",
                        "description": "Optional metadata for the note",
                        "additionalProperties": True
                    },
                    "access_control": {
                        "type": "object",
                        "description": "Optional access control settings",
                        "additionalProperties": True
                    }
                },
                "required": ["title"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_note_notes_create operation."""
        self._log_execution_start(arguments)

        # Build request with NoteForm schema
        json_data = {
            "title": arguments.get("title")
        }
        if arguments.get("data"):
            json_data["data"] = arguments.get("data")
        if arguments.get("meta"):
            json_data["meta"] = arguments.get("meta")
        if arguments.get("access_control"):
            json_data["access_control"] = arguments.get("access_control")

        response = await self.client.post("/api/v1/notes/create", json_data=json_data)

        self._log_execution_end(response)
        return response