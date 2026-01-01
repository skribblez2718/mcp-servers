"""Update Embedding Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateEmbeddingConfigRetrievalEmbeddingUpdateTool(BaseTool):
    """Update Embedding Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_embedding_config_retrieval_embedding_update",
            "description": "Update Embedding Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "embedding_engine": {"type": "string", "description": "Embedding engine to use"},
                    "embedding_model": {"type": "string", "description": "Embedding model to use"},
                    "embedding_batch_size": {"type": ["integer", "null"], "description": "Batch size for embeddings", "default": 1},
                    "openai_config": {
                        "type": ["object", "null"],
                        "description": "OpenAI config with url and key",
                        "properties": {
                            "url": {"type": "string"},
                            "key": {"type": "string"}
                        }
                    },
                    "ollama_config": {
                        "type": ["object", "null"],
                        "description": "Ollama config with url and key",
                        "properties": {
                            "url": {"type": "string"},
                            "key": {"type": "string"}
                        }
                    },
                    "azure_openai_config": {
                        "type": ["object", "null"],
                        "description": "Azure OpenAI config with url, key, and version",
                        "properties": {
                            "url": {"type": "string"},
                            "key": {"type": "string"},
                            "version": {"type": "string"}
                        }
                    }
                },
                "required": ["embedding_engine", "embedding_model"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_embedding_config_retrieval_embedding_update operation."""
        self._log_execution_start(arguments)

        # Build request - Note: API expects RAG_EMBEDDING_* field names despite OpenAPI spec
        json_data = {
            "RAG_EMBEDDING_ENGINE": arguments["embedding_engine"],
            "RAG_EMBEDDING_MODEL": arguments["embedding_model"]
        }
        if arguments.get("embedding_batch_size") is not None:
            json_data["RAG_EMBEDDING_BATCH_SIZE"] = arguments["embedding_batch_size"]
        if arguments.get("openai_config") is not None:
            json_data["openai_config"] = arguments["openai_config"]
        if arguments.get("ollama_config") is not None:
            json_data["ollama_config"] = arguments["ollama_config"]
        if arguments.get("azure_openai_config") is not None:
            json_data["azure_openai_config"] = arguments["azure_openai_config"]

        response = await self.client.post("/api/v1/retrieval/embedding/update", json_data=json_data)

        self._log_execution_end(response)
        return response