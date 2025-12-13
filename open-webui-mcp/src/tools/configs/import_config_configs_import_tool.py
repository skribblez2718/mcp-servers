"""Import Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ImportConfigConfigsImportTool(BaseTool):
    """Import Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "import_config_configs_import",
            "description": "Import Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute import_config_configs_import operation."""
        self._log_execution_start(arguments)



        # Build request
        json_data = {}

        response = await self.client.post("/api/v1/configs/import", json_data=json_data)

        self._log_execution_end(response)
        return response