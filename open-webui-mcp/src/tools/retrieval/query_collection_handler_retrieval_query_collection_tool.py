"""Query Collection Handler"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class QueryCollectionHandlerRetrievalQueryCollectionTool(BaseTool):
    """Query Collection Handler"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "query_collection_handler_retrieval_query_collection",
            "description": "Query multiple collections for RAG retrieval",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "collection_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of collection names to query"
                    },
                    "query": {"type": "string", "description": "Query string"},
                    "k": {"type": ["integer", "null"], "description": "Number of results to return"},
                    "k_reranker": {"type": ["integer", "null"], "description": "Number of results for reranker"},
                    "r": {"type": ["number", "null"], "description": "Relevance threshold"},
                    "hybrid": {"type": ["boolean", "null"], "description": "Enable hybrid search"},
                    "hybrid_bm25_weight": {"type": ["number", "null"], "description": "BM25 weight for hybrid search"}
                },
                "required": ["collection_names", "query"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute query_collection_handler_retrieval_query_collection operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "collection_names": arguments["collection_names"],
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
        if arguments.get("hybrid_bm25_weight") is not None:
            json_data["hybrid_bm25_weight"] = arguments["hybrid_bm25_weight"]

        response = await self.client.post("/api/v1/retrieval/query/collection", json_data=json_data)

        self._log_execution_end(response)
        return response