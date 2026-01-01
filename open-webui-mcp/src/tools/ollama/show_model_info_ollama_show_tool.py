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
                    "model": {
                        "type": ["string", "null"],
                        "description": "Name of the model to show info for"
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute show_model_info_ollama_show operation."""
        self._log_execution_start(arguments)



        # Build request body - ModelNameForm with additionalProperties
        json_data = {}
        if arguments.get("model") is not None:
            json_data["model"] = arguments["model"]
        # Pass through any additional properties
        for key, value in arguments.items():
            if key != "model" and value is not None:
                json_data[key] = value

        response = await self.client.post("/ollama/api/show", json_data=json_data)

        self._log_execution_end(response)
        return response