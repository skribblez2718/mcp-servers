"""Load Tool From Url"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class LoadToolFromUrlToolsLoadUrlTool(BaseTool):
    """Load Tool From Url"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "load_tool_from_url_tools_load_url",
            "description": "Load Tool From Url",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute load_tool_from_url_tools_load_url operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/tools/load/url", json_data=json_data)

        self._log_execution_end(response)
        return response