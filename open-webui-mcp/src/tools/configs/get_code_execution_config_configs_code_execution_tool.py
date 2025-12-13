"""Get Code Execution Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class GetCodeExecutionConfigConfigsCodeExecutionTool(BaseTool):
    """Get Code Execution Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "get_code_execution_config_configs_code_execution",
            "description": "Get Code Execution Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute get_code_execution_config_configs_code_execution operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/configs/code_execution", params=params)

        self._log_execution_end(response)
        return response