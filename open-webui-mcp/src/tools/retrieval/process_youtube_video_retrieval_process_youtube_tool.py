"""Process Youtube Video"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ProcessYoutubeVideoRetrievalProcessYoutubeTool(BaseTool):
    """Process Youtube Video"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "process_youtube_video_retrieval_process_youtube",
            "description": "Process Youtube Video for RAG retrieval",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "YouTube video URL to process"},
                    "collection_name": {"type": ["string", "null"], "description": "Collection name to store in"}
                },
                "required": ["url"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute process_youtube_video_retrieval_process_youtube operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {"url": arguments["url"]}
        if arguments.get("collection_name") is not None:
            json_data["collection_name"] = arguments["collection_name"]

        response = await self.client.post("/api/v1/retrieval/process/youtube", json_data=json_data)

        self._log_execution_end(response)
        return response