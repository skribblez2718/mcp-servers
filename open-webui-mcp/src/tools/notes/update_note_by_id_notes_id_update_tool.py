"""Update Note By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateNoteByIdNotesIdUpdateTool(BaseTool):
    """Update Note By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_note_by_id_notes_id_update",
            "description": "Update Note By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The note ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "The new title of the note"
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
                "required": ["id", "title"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_note_by_id_notes_id_update operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: id
        id = arguments.get("id")
        if id:
            id = ToolInputValidator.validate_id(id, "id")

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

        response = await self.client.post(f"/api/v1/notes/{id}/update", json_data=json_data)

        self._log_execution_end(response)
        return response