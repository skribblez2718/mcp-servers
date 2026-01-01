"""Query Doc Handler"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class QueryDocHandlerRetrievalQueryDocTool(BaseTool):
    """Query Doc Handler"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "query_doc_handler_retrieval_query_doc",
            "description": "Query a document collection for RAG retrieval",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "collection_name": {"type": "string", "description": "Collection name to query"},
                    "query": {"type": "string", "description": "Query string"},
                    "k": {"type": ["integer", "null"], "description": "Number of results to return"},
                    "k_reranker": {"type": ["integer", "null"], "description": "Number of results for reranker"},
                    "r": {"type": ["number", "null"], "description": "Relevance threshold"},
                    "hybrid": {"type": ["boolean", "null"], "description": "Enable hybrid search"}
                },
                "required": ["collection_name", "query"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute query_doc_handler_retrieval_query_doc operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "collection_name": arguments["collection_name"],
            "query": arguments["query"]
        }
        if arguments.get("k") is not None:
            json_data["k"] = arguments["k"]
        if arguments.get("k_reranker") is not None:
            json_data["k_reranker"] = arguments["k_reranker"]
        if arguments.get("r") is not None:
            json_data["r"] = arguments["r"]
        if arguments.get("hybrid") is not None:
            json_data["hybrid"] = arguments["hybrid"]

        response = await self.client.post("/api/v1/retrieval/query/doc", json_data=json_data)

        self._log_execution_end(response)
        return response