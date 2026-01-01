"""Update Default User Permissions"""

from typing import Any
from src.tools.base import BaseTool
from src.utils.validation import ToolInputValidator


class UpdateDefaultUserPermissionsUsersDefaultPermissionsTool(BaseTool):
    """Update Default User Permissions"""

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "update_default_user_permissions_users_default_permissions",
            "description": "Update Default User Permissions",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "workspace": {
                        "type": "object",
                        "description": "Workspace permissions",
                        "properties": {
                            "models": {"type": "boolean", "description": "Access to models"},
                            "knowledge": {"type": "boolean", "description": "Access to knowledge"},
                            "prompts": {"type": "boolean", "description": "Access to prompts"},
                            "tools": {"type": "boolean", "description": "Access to tools"}
                        }
                    },
                    "sharing": {
                        "type": "object",
                        "description": "Sharing permissions",
                        "properties": {
                            "public_models": {"type": "boolean", "description": "Can share models publicly"},
                            "public_knowledge": {"type": "boolean", "description": "Can share knowledge publicly"},
                            "public_prompts": {"type": "boolean", "description": "Can share prompts publicly"},
                            "public_tools": {"type": "boolean", "description": "Can share tools publicly"}
                        }
                    },
                    "chat": {
                        "type": "object",
                        "description": "Chat permissions",
                        "properties": {
                            "controls": {"type": "boolean"},
                            "system_prompt": {"type": "boolean"},
                            "file_upload": {"type": "boolean"},
                            "delete": {"type": "boolean"},
                            "edit": {"type": "boolean"},
                            "share": {"type": "boolean"},
                            "export": {"type": "boolean"},
                            "stt": {"type": "boolean"},
                            "tts": {"type": "boolean"},
                            "call": {"type": "boolean"},
                            "multiple_models": {"type": "boolean"},
                            "temporary": {"type": "boolean"},
                            "temporary_enforced": {"type": "boolean"}
                        }
                    },
                    "features": {
                        "type": "object",
                        "description": "Feature permissions",
                        "properties": {
                            "direct_tool_servers": {"type": "boolean"},
                            "web_search": {"type": "boolean"},
                            "image_generation": {"type": "boolean"},
                            "code_interpreter": {"type": "boolean"},
                            "notes": {"type": "boolean"}
                        }
                    }
                },
                "required": ["workspace", "sharing", "chat", "features"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute update_default_user_permissions_users_default_permissions operation."""
        self._log_execution_start(arguments)

        # Build request
        json_data = {
            "workspace": arguments.get("workspace", {}),
            "sharing": arguments.get("sharing", {}),
            "chat": arguments.get("chat", {}),
            "features": arguments.get("features", {})
        }

        response = await self.client.post("/api/v1/users/default/permissions", json_data=json_data)

        self._log_execution_end(response)
        return response