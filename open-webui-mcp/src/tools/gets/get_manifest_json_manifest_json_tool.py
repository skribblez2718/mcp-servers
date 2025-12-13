"""Get Manifest Json"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetManifestJsonManifestJsonTool(BaseTool):
    """Get Manifest Json"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_manifest_json_manifest_json",
            "description": "Get Manifest Json",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_manifest_json_manifest_json operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/manifest.json", params=params)

        self._log_execution_end(response)
        return response