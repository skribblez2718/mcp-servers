"""Update Rag Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateRagConfigRetrievalConfigUpdateTool(BaseTool):
    """Update Rag Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_rag_config_retrieval_config_update",
            "description": "Update Rag Config - all fields are optional",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "RAG_TEMPLATE": {"type": ["string", "null"], "description": "RAG template"},
                    "TOP_K": {"type": ["integer", "null"], "description": "Top K results"},
                    "BYPASS_EMBEDDING_AND_RETRIEVAL": {"type": ["boolean", "null"], "description": "Bypass embedding and retrieval"},
                    "RAG_FULL_CONTEXT": {"type": ["boolean", "null"], "description": "Use full RAG context"},
                    "ENABLE_RAG_HYBRID_SEARCH": {"type": ["boolean", "null"], "description": "Enable hybrid search"},
                    "TOP_K_RERANKER": {"type": ["integer", "null"], "description": "Top K for reranker"},
                    "RELEVANCE_THRESHOLD": {"type": ["number", "null"], "description": "Relevance threshold"},
                    "HYBRID_BM25_WEIGHT": {"type": ["number", "null"], "description": "Hybrid BM25 weight"},
                    "CONTENT_EXTRACTION_ENGINE": {"type": ["string", "null"], "description": "Content extraction engine"},
                    "PDF_EXTRACT_IMAGES": {"type": ["boolean", "null"], "description": "Extract images from PDF"},
                    "RAG_RERANKING_MODEL": {"type": ["string", "null"], "description": "Reranking model"},
                    "RAG_RERANKING_ENGINE": {"type": ["string", "null"], "description": "Reranking engine"},
                    "TEXT_SPLITTER": {"type": ["string", "null"], "description": "Text splitter type"},
                    "CHUNK_SIZE": {"type": ["integer", "null"], "description": "Chunk size"},
                    "CHUNK_OVERLAP": {"type": ["integer", "null"], "description": "Chunk overlap"},
                    "FILE_MAX_SIZE": {"type": ["integer", "null"], "description": "Max file size"},
                    "FILE_MAX_COUNT": {"type": ["integer", "null"], "description": "Max file count"},
                    "web": {"type": ["object", "null"], "description": "Web search configuration", "additionalProperties": True}
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_rag_config_retrieval_config_update operation."""
        self._log_execution_start(arguments)

        # Build request - all fields are optional, pass them through directly
        json_data = {k: v for k, v in arguments.items() if v is not None}

        response = await self.client.post("/api/v1/retrieval/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response