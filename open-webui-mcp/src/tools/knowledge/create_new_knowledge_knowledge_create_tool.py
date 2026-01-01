"""Create New Knowledge"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewKnowledgeKnowledgeCreateTool(BaseTool):
    """Create New Knowledge"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_knowledge_knowledge_create",
            "description": "Create New Knowledge",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the knowledge base"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the knowledge base"
                    },
                    "data": {
                        "type": ["object", "null"],
                        "additionalProperties": True,
                        "description": "Optional additional data"
                    },
                    "access_control": {
                        "type": ["object", "null"],
                        "additionalProperties": True,
                        "description": "Optional access control settings"
                    }
                },
                "required": ["name", "description"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_knowledge_knowledge_create operation."""
        self._log_execution_start(arguments)

        # Build request with KnowledgeForm
        json_data = {
            "name": arguments.get("name"),
            "description": arguments.get("description")
        }

        # Add optional fields if provided
        if arguments.get("data") is not None:
            json_data["data"] = arguments.get("data")
        if arguments.get("access_control") is not None:
            json_data["access_control"] = arguments.get("access_control")

        response = await self.client.post("/api/v1/knowledge/create", json_data=json_data)

        self._log_execution_end(response)
        return response