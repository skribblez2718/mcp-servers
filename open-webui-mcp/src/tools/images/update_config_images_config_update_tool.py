"""Update Config"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateConfigImagesConfigUpdateTool(BaseTool):
    """Update Config"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_config_images_config_update",
            "description": "Update Config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "description": "Whether image generation is enabled"
                    },
                    "engine": {
                        "type": "string",
                        "description": "The image generation engine to use (e.g., 'openai', 'automatic1111', 'comfyui', 'gemini')"
                    },
                    "prompt_generation": {
                        "type": "boolean",
                        "description": "Whether to enable prompt generation/enhancement"
                    },
                    "openai": {
                        "type": "object",
                        "description": "OpenAI configuration",
                        "properties": {
                            "OPENAI_API_BASE_URL": {"type": "string"},
                            "OPENAI_API_KEY": {"type": "string"}
                        },
                        "required": ["OPENAI_API_BASE_URL", "OPENAI_API_KEY"]
                    },
                    "automatic1111": {
                        "type": "object",
                        "description": "Automatic1111 configuration",
                        "properties": {
                            "AUTOMATIC1111_BASE_URL": {"type": "string"},
                            "AUTOMATIC1111_API_AUTH": {"type": "string"},
                            "AUTOMATIC1111_CFG_SCALE": {"type": ["string", "number", "null"]},
                            "AUTOMATIC1111_SAMPLER": {"type": ["string", "null"]},
                            "AUTOMATIC1111_SCHEDULER": {"type": ["string", "null"]}
                        },
                        "required": ["AUTOMATIC1111_BASE_URL", "AUTOMATIC1111_API_AUTH", "AUTOMATIC1111_CFG_SCALE", "AUTOMATIC1111_SAMPLER", "AUTOMATIC1111_SCHEDULER"]
                    },
                    "comfyui": {
                        "type": "object",
                        "description": "ComfyUI configuration",
                        "properties": {
                            "COMFYUI_BASE_URL": {"type": "string"},
                            "COMFYUI_API_KEY": {"type": "string"},
                            "COMFYUI_WORKFLOW": {"type": "string"},
                            "COMFYUI_WORKFLOW_NODES": {"type": "array", "items": {"type": "object"}}
                        },
                        "required": ["COMFYUI_BASE_URL", "COMFYUI_API_KEY", "COMFYUI_WORKFLOW", "COMFYUI_WORKFLOW_NODES"]
                    },
                    "gemini": {
                        "type": "object",
                        "description": "Gemini configuration",
                        "properties": {
                            "GEMINI_API_BASE_URL": {"type": "string"},
                            "GEMINI_API_KEY": {"type": "string"}
                        },
                        "required": ["GEMINI_API_BASE_URL", "GEMINI_API_KEY"]
                    }
                },
                "required": ["enabled", "engine", "prompt_generation", "openai", "automatic1111", "comfyui", "gemini"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_config_images_config_update operation."""
        self._log_execution_start(arguments)

        # Build request with full ConfigForm structure
        json_data = {
            "enabled": arguments.get("enabled"),
            "engine": arguments.get("engine"),
            "prompt_generation": arguments.get("prompt_generation"),
            "openai": arguments.get("openai"),
            "automatic1111": arguments.get("automatic1111"),
            "comfyui": arguments.get("comfyui"),
            "gemini": arguments.get("gemini")
        }

        response = await self.client.post("/api/v1/images/config/update", json_data=json_data)

        self._log_execution_end(response)
        return response