"""Process Text"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ProcessTextRetrievalProcessTextTool(BaseTool):
    """Process Text"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "process_text_retrieval_process_text",
            "description": "Process Text for RAG retrieval",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name for the text document"},
                    "content": {"type": "string", "description": "Text content to process"},
                    "collection_name": {"type": ["string", "null"], "description": "Collection name to store in"}
                },
                "required": ["name", "content"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute process_text_retrieval_process_text operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "name": arguments["name"],
            "content": arguments["content"]
        }
        if arguments.get("collection_name") is not None:
            json_data["collection_name"] = arguments["collection_name"]

        response = await self.client.post("/api/v1/retrieval/process/text", json_data=json_data)

        self._log_execution_end(response)
        return response