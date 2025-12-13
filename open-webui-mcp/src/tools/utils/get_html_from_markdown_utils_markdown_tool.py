"""Get Html From Markdown"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetHtmlFromMarkdownUtilsMarkdownTool(BaseTool):
    """Get Html From Markdown"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_html_from_markdown_utils_markdown",
            "description": "Get Html From Markdown",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_html_from_markdown_utils_markdown operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/utils/markdown", json_data=json_data)

        self._log_execution_end(response)
        return response