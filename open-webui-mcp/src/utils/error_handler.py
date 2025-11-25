"""Error handling and sanitization utilities.

Transforms exceptions into safe error messages for MCP clients.
"""

import logging
from typing import Any
from src.exceptions import (
    HTTPError,
    RateLimitError,
    AuthError,
    NotFoundError,
    ValidationError,
    ServerError
)

logger = logging.getLogger(__name__)


def sanitize_error(exception: Exception, user_message: str) -> dict[str, Any]:
    """Sanitize error for client response.

    Logs full exception details but returns safe message to user.

    Args:
        exception: The exception that occurred
        user_message: User-friendly message

    Returns:
        Safe error dict for MCP response
    """
    # Log full exception with stack trace
    logger.error(
        f"Error occurred: {exception}",
        exc_info=True,
        extra={"exception_type": type(exception).__name__}
    )

    # Build safe error response
    error_data: dict[str, Any] = {
        "error": user_message,
        "type": type(exception).__name__,
    }

    # Add status code for HTTP errors
    if isinstance(exception, HTTPError):
        error_data["status_code"] = exception.status_code

    # Add retry_after for rate limit errors
    if isinstance(exception, RateLimitError):
        error_data["retry_after"] = exception.retry_after

    return error_data


def transform_http_status_to_exception(status_code: int, message: str) -> HTTPError:
    """Transform HTTP status code to appropriate exception.

    Args:
        status_code: HTTP status code
        message: Error message

    Returns:
        Appropriate HTTPError subclass
    """
    if status_code == 400:
        return ValidationError(message)
    elif status_code == 401:
        return AuthError(message, status_code=401)
    elif status_code == 403:
        return AuthError(message, status_code=403)
    elif status_code == 404:
        return NotFoundError(message)
    elif status_code == 429:
        return RateLimitError(message)
    elif status_code >= 500:
        return ServerError(message, status_code=status_code)
    else:
        return HTTPError(message, status_code=status_code)
