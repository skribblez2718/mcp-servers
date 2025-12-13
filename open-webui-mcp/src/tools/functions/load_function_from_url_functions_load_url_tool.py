"""Load Function From Url"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class LoadFunctionFromUrlFunctionsLoadUrlTool(BaseTool):
    """Load Function From Url"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "load_function_from_url_functions_load_url",
            "description": "Load Function From Url",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute load_function_from_url_functions_load_url operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/functions/load/url", json_data=json_data)

        self._log_execution_end(response)
        return response