"""Format Code"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class FormatCodeUtilsCodeFormatTool(BaseTool):
    """Format Code"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "format_code_utils_code_format",
            "description": "Format Code",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The code to format"
                    }
                },
                "required": ["code"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute format_code_utils_code_format operation."""
        self._log_execution_start(arguments)

        # Build request body per CodeForm schema
        json_data = {
            "code": arguments.get("code")
        }

        response = await self.client.post("/api/v1/utils/code/format", json_data=json_data)

        self._log_execution_end(response)
        return response