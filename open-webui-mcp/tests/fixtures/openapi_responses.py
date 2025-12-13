"""Mock responses based on OpenAPI spec examples.

Provides realistic mock data extracted from Open WebUI OpenAPI documentation.
"""

from datetime import datetime
from typing import Any


class OpenAPIResponses:
    """Realistic mock responses from OpenAPI spec."""

    @staticmethod
    def chat_list(count: int = 3) -> dict[str, Any]:
        """Chat list response.

        Args:
            count: Number of chats to return

        Returns:
            Realistic chat list response
        """
        chats = [
            {
                "id": f"chat-{i}",
                "user_id": "user-123",
                "title": f"Chat {i}",
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:30:00Z",
                "messages": [],
                "metadata": {
                    "tags": ["test"],
                    "archived": False
                }
            }
            for i in range(count)
        ]

        return {
            "data": chats,
            "total": count,
            "limit": 10,
            "offset": 0,
            "has_next": False
        }

    @staticmethod
    def chat_get(chat_id: str = "chat-123") -> dict[str, Any]:
        """Single chat response.

        Args:
            chat_id: Chat ID

        Returns:
            Realistic chat detail response
        """
        return {
            "id": chat_id,
            "user_id": "user-123",
            "title": "Test Conversation",
            "created_at": "2025-01-01T12:00:00Z",
            "updated_at": "2025-01-01T12:30:00Z",
            "messages": [
                {
                    "id": "msg-1",
                    "role": "user",
                    "content": "Hello",
                    "created_at": "2025-01-01T12:00:00Z"
                },
                {
                    "id": "msg-2",
                    "role": "assistant",
                    "content": "Hi! How can I help you?",
                    "created_at": "2025-01-01T12:00:05Z"
                }
            ],
            "metadata": {
                "tags": ["conversation"],
                "archived": False,
                "shared": False
            }
        }

    @staticmethod
    def model_list(count: int = 3) -> dict[str, Any]:
        """Model list response.

        Args:
            count: Number of models

        Returns:
            Realistic model list response
        """
        models = [
            {
                "id": f"model-{i}:latest",
                "name": f"Model {i}",
                "size": 3800000000 + (i * 1000000),
                "digest": f"sha256:abc{i}",
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-01T10:00:00Z"
            }
            for i in range(count)
        ]

        return {
            "data": models,
            "total": count,
            "limit": 10,
            "offset": 0,
            "has_next": False
        }

    @staticmethod
    def user_list(count: int = 2) -> dict[str, Any]:
        """User list response.

        Args:
            count: Number of users

        Returns:
            Realistic user list response
        """
        users = [
            {
                "id": f"user-{i}",
                "email": f"user{i}@example.com",
                "name": f"User {i}",
                "role": "user" if i > 0 else "admin",
                "created_at": "2024-12-01T00:00:00Z",
                "updated_at": "2024-12-01T00:00:00Z"
            }
            for i in range(count)
        ]

        return {
            "data": users,
            "total": count,
            "limit": 10,
            "offset": 0,
            "has_next": False
        }

    @staticmethod
    def health_check() -> dict[str, Any]:
        """Health check response.

        Returns:
            Health check status
        """
        return {
            "status": "healthy",
            "version": "0.1.0",
            "database": "connected",
            "uptime_seconds": 3600
        }

    @staticmethod
    def error_response(
        status_code: int,
        message: str,
        error_type: str = "error"
    ) -> dict[str, Any]:
        """Error response.

        Args:
            status_code: HTTP status code
            message: Error message
            error_type: Error type identifier

        Returns:
            Error response structure
        """
        return {
            "error": message,
            "type": error_type,
            "status_code": status_code
        }

    @staticmethod
    def rate_limit_error() -> dict[str, Any]:
        """Rate limit exceeded error.

        Returns:
            429 rate limit error
        """
        return OpenAPIResponses.error_response(
            429,
            "Rate limit exceeded. Please try again later.",
            "rate_limit_error"
        )

    @staticmethod
    def not_found_error(resource: str = "resource") -> dict[str, Any]:
        """Not found error.

        Args:
            resource: Resource type

        Returns:
            404 not found error
        """
        return OpenAPIResponses.error_response(
            404,
            f"{resource.capitalize()} not found",
            "not_found_error"
        )

    @staticmethod
    def validation_error(field: str, message: str) -> dict[str, Any]:
        """Validation error.

        Args:
            field: Field that failed validation
            message: Validation error message

        Returns:
            400 validation error
        """
        return {
            "error": "Validation failed",
            "type": "validation_error",
            "status_code": 400,
            "details": [
                {
                    "field": field,
                    "message": message
                }
            ]
        }

    @staticmethod
    def server_error() -> dict[str, Any]:
        """Internal server error.

        Returns:
            500 server error
        """
        return OpenAPIResponses.error_response(
            500,
            "Internal server error",
            "server_error"
        )
