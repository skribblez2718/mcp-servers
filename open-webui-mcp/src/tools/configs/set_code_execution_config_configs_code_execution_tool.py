"""Set Code Execution Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class SetCodeExecutionConfigConfigsCodeExecutionTool(BaseTool):
    """Set Code Execution Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "set_code_execution_config_configs_code_execution",
            "description": "Set Code Execution Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute set_code_execution_config_configs_code_execution operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/configs/code_execution", json_data=json_data)

        self._log_execution_end(response)
        return response