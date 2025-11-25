"""Model list tool - List all available models."""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class ModelListTool(BaseTool):
    """List all available models.

    Retrieves list of models with pagination support.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition with schema
        """
        return {
            "name": "model_list",
            "description": "List all available models with pagination",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of models to return (1-1000)",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset in the list",
                        "default": 0,
                        "minimum": 0
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute model list retrieval.

        Args:
            arguments: Tool arguments with limit, offset

        Returns:
            Dict with models list

        Raises:
            ValidationError: If arguments invalid
            HTTPError: If API call fails
        """
        self._log_execution_start(arguments)

        # Extract and validate
        limit = arguments.get("limit", 50)
        offset = arguments.get("offset", 0)

        limit, offset = ToolInputValidator.validate_pagination(limit, offset)

        # Call API
        params = {"limit": limit, "offset": offset}
        response_data = await self.client.get("/api/v1/models/", params=params)

        result = {
            "models": response_data.get("data", response_data.get("models", [])),
            "total": response_data.get("total", len(response_data.get("data", []))),
            "limit": limit,
            "offset": offset
        }

        self._log_execution_end(result)

        return result
