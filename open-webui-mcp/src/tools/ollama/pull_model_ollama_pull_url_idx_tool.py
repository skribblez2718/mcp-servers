"""Pull Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class PullModelOllamaPullUrlIdxTool(BaseTool):
    """Pull Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "pull_model_ollama_pull_url_idx",
            "description": "Pull Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url_idx": {
                        "type": "integer",
                        "description": ""
                    }
                },
                "required": ["url_idx"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute pull_model_ollama_pull_url_idx operation."""
        self._log_execution_start(arguments)

        # Validate path parameter: url_idx
        url_idx = arguments.get("url_idx")
        if url_idx:
            url_idx = ToolInputValidator.validate_id(url_idx, "url_idx")


        # Build request
        json_data = {}

        response = await self.client.post(f"/ollama/api/pull/{url_idx}", json_data=json_data)

        self._log_execution_end(response)
        return response