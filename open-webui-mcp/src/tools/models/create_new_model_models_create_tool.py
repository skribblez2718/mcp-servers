"""Create New Model"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class CreateNewModelModelsCreateTool(BaseTool):
    """Create New Model"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "create_new_model_models_create",
            "description": "Create New Model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The model ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "The model name"
                    },
                    "meta": {
                        "type": "object",
                        "description": "Model metadata",
                        "additionalProperties": True,
                        "properties": {
                            "profile_image_url": {
                                "type": ["string", "null"],
                                "description": "Profile image URL",
                                "default": "/static/favicon.png"
                            },
                            "description": {
                                "type": ["string", "null"],
                                "description": "Model description"
                            },
                            "capabilities": {
                                "type": ["object", "null"],
                                "additionalProperties": True,
                                "description": "Model capabilities"
                            }
                        }
                    },
                    "params": {
                        "type": "object",
                        "description": "Model parameters",
                        "additionalProperties": True
                    },
                    "base_model_id": {
                        "type": ["string", "null"],
                        "description": "Base model ID (optional)"
                    },
                    "access_control": {
                        "type": ["object", "null"],
                        "additionalProperties": True,
                        "description": "Access control settings (optional)"
                    },
                    "is_active": {
                        "type": "boolean",
                        "description": "Whether the model is active (default: true)",
                        "default": True
                    }
                },
                "required": ["id", "name", "meta", "params"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute create_new_model_models_create operation."""
        self._log_execution_start(arguments)

        # Build request with ModelForm
        json_data = {
            "id": arguments.get("id"),
            "name": arguments.get("name"),
            "meta": arguments.get("meta", {}),
            "params": arguments.get("params", {})
        }

        # Add optional fields if provided
        if arguments.get("base_model_id") is not None:
            json_data["base_model_id"] = arguments.get("base_model_id")
        if arguments.get("access_control") is not None:
            json_data["access_control"] = arguments.get("access_control")
        if "is_active" in arguments:
            json_data["is_active"] = arguments.get("is_active")

        response = await self.client.post("/api/v1/models/create", json_data=json_data)

        self._log_execution_end(response)
        return response