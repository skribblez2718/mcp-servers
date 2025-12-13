"""API key management tools for managed API key operations."""

import time
from typing import Any, Dict

from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import log_tool_execution


class ApiKeysManageTool(BaseTool):
    """Manage API keys: create, list, and delete."""

    def name(self) -> str:
        """Return tool name."""
        return "recipez_api_keys_manage"

    def description(self) -> str:
        """Return tool description."""
        return (
            "Manage managed API keys. "
            "Operations: 'create' (new key), 'list' (all keys), 'delete' (remove key). "
            "JWT tokens are only returned once at creation."
        )

    def input_schema(self) -> Dict[str, Any]:
        """Return input schema."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["create", "list", "delete"],
                    "description": "Operation to perform",
                },
                "name": {
                    "type": "string",
                    "description": "API key name (required for create)",
                },
                "scopes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Permission scopes (required for create)",
                },
                "expires_at": {
                    "type": "string",
                    "description": "Expiration timestamp ISO 8601 (optional for create)",
                },
                "never_expires": {
                    "type": "boolean",
                    "description": "Set to true for keys that never expire (optional for create)",
                },
                "api_key_id": {
                    "type": "string",
                    "description": "API key UUID (required for delete)",
                },
            },
            "required": ["operation"],
        }

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API key management operation.

        Args:
            params: Dictionary with operation and operation-specific parameters

        Returns:
            Operation result
        """
        start = time.time()
        operation = params["operation"]

        try:
            if operation == "create":
                payload = {
                    "name": params["name"],
                    "scopes": params["scopes"],
                }
                if params.get("expires_at"):
                    payload["expires_at"] = params["expires_at"]
                if params.get("never_expires"):
                    payload["never_expires"] = params["never_expires"]

                result = await self.http_client.post(
                    "/api/profile/api-keys",
                    json=payload,
                )
            elif operation == "list":
                result = await self.http_client.get("/api/profile/api-keys")
            elif operation == "delete":
                api_key_id = params["api_key_id"]
                result = await self.http_client.delete(
                    f"/api/profile/api-keys/{api_key_id}"
                )
            else:
                raise ValueError(f"Invalid operation: {operation}")

            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                operation,
                duration,
                "success",
            )
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            log_tool_execution(
                self.logger,
                self.name(),
                operation,
                duration,
                "error",
                error=str(e),
            )
            raise
