"""Verify Connection"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class VerifyConnectionOllamaVerifyTool(BaseTool):
    """Verify Connection"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "verify_connection_ollama_verify",
            "description": "Verify Ollama Connection",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Ollama server URL"},
                    "key": {"type": ["string", "null"], "description": "Optional API key"}
                },
                "required": ["url"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute verify_connection_ollama_verify operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {"url": arguments["url"]}
        if arguments.get("key") is not None:
            json_data["key"] = arguments["key"]

        response = await self.client.post("/ollama/verify", json_data=json_data)

        self._log_execution_end(response)
        return response