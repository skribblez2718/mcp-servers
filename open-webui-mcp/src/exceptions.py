"""Custom exception hierarchy for Open WebUI MCP Server.

This module defines domain-specific exceptions that map HTTP status codes
to meaningful error types for better error handling and debugging.
"""

from typing import Any


class HTTPError(Exception):
    """Base exception for HTTP errors.

    Args:
        message: Human-readable error message
        status_code: HTTP status code
        response: Optional response data
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        response: dict[str, Any] | None = None
    ) -> None:
        """Initialize HTTP error.

        Args:
            message: Error message
            status_code: HTTP status code
            response: Optional response data
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response or {}

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__} ({self.status_code}): {self.message}"


class RateLimitError(HTTPError):
    """Rate limit exceeded (429).

    Args:
        message: Error message
        retry_after: Seconds to wait before retry
    """

    def __init__(self, message: str, retry_after: int = 60) -> None:
        """Initialize rate limit error.

        Args:
            message: Error message
            retry_after: Seconds to wait before retry
        """
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class AuthError(HTTPError):
    """Authentication failed (401/403).

    Args:
        message: Error message
        status_code: 401 (unauthorized) or 403 (forbidden)
    """

    def __init__(self, message: str, status_code: int = 401) -> None:
        """Initialize auth error.

        Args:
            message: Error message
            status_code: HTTP status code
        """
        super().__init__(message, status_code=status_code)


class NotFoundError(HTTPError):
    """Resource not found (404).

    Args:
        message: Error message
    """

    def __init__(self, message: str) -> None:
        """Initialize not found error.

        Args:
            message: Error message
        """
        super().__init__(message, status_code=404)


class ValidationError(HTTPError):
    """Input validation failed (400).

    Args:
        message: Error message
        errors: Optional list of validation errors
    """

    def __init__(
        self,
        message: str,
        errors: list[dict[str, Any]] | None = None
    ) -> None:
        """Initialize validation error.

        Args:
            message: Error message
            errors: Optional list of validation errors
        """
        super().__init__(message, status_code=400)
        self.errors = errors or []


class ServerError(HTTPError):
    """Server error (5xx).

    Args:
        message: Error message
        status_code: HTTP 5xx status code
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        """Initialize server error.

        Args:
            message: Error message
            status_code: HTTP status code
        """
        super().__init__(message, status_code=status_code)
