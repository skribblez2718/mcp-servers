"""Show Model Info"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ShowModelInfoOllamaShowTool(BaseTool):
    """Show Model Info"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "show_model_info_ollama_show",
            "description": "Show Model Info",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute show_model_info_ollama_show operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/ollama/api/show", json_data=json_data)

        self._log_execution_end(response)
        return response