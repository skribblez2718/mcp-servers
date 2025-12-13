"""Download Litellm Config Yaml"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class DownloadLitellmConfigYamlUtilsLitellmConfigTool(BaseTool):
    """Download Litellm Config Yaml"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "download_litellm_config_yaml_utils_litellm_config",
            "description": "Download Litellm Config Yaml",
            "inputSchema": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute download_litellm_config_yaml_utils_litellm_config operation."""
        self._log_execution_start(arguments)



        # Build request
        params = {}

        response = await self.client.get("/api/v1/utils/litellm/config", params=params)

        self._log_execution_end(response)
        return response