"""Update Model By Id"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateModelByIdModelsModelUpdateTool(BaseTool):
    """Update Model By Id"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_model_by_id_models_model_update",
            "description": "Update Model By Id",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The model ID (query parameter)"
                    },
                    "model_id": {
                        "type": "string",
                        "description": "The model ID in the body (usually same as query id)"
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
                "required": ["id", "model_id", "name", "meta", "params"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_model_by_id_models_model_update operation."""
        self._log_execution_start(arguments)

        # Query parameter: id
        id = arguments.get("id")

        # Build request with ModelForm body
        json_data = {
            "id": arguments.get("model_id"),
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

        response = await self.client.post("/api/v1/models/model/update", params={"id": id}, json_data=json_data)

        self._log_execution_end(response)
        return response