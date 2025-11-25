"""Tests for error handling utilities.

Tests error message sanitization and HTTP error transformation.
"""

import pytest
from unittest.mock import Mock
import httpx
from src.utils.error_handler import sanitize_error, transform_http_status_to_exception
from src.exceptions import (
    HTTPError,
    RateLimitError,
    AuthError,
    NotFoundError,
    ValidationError,
    ServerError
)


class TestErrorHandler:
    """Test error handling utilities."""

    def test_sanitize_error_generic_exception(self):
        """Test sanitizing generic exception."""
        error = Exception("Internal details here")

        result = sanitize_error(error, "Operation failed")

        assert result["error"] == "Operation failed"
        assert "type" in result
        assert "Internal details" not in result["error"]

    def test_sanitize_error_http_error(self):
        """Test sanitizing HTTPError."""
        error = HTTPError(
            message="Detailed internal error",
            status_code=500
        )

        result = sanitize_error(error, "Request failed")

        assert result["error"] == "Request failed"
        assert result["status_code"] == 500
        assert "Detailed internal" not in result["error"]

    def test_sanitize_error_validation_error(self):
        """Test sanitizing ValidationError with details."""
        error = ValidationError(
            message="Validation failed",
            errors=[{"field": "limit", "message": "too large"}]
        )

        result = sanitize_error(error, "Invalid input")

        assert result["error"] == "Invalid input"
        assert result["status_code"] == 400
        # Sanitized error shouldn't leak internal validation details
        assert "errors" not in result or result.get("errors") == []

    def test_sanitize_error_preserves_type(self):
        """Test sanitize preserves error type."""
        error = RateLimitError("Rate limited", retry_after=60)

        result = sanitize_error(error, "Too many requests")

        assert result["error"] == "Too many requests"
        assert result["type"] == "RateLimitError"
        assert result["status_code"] == 429

    def test_transform_http_status_400(self):
        """Test transforming 400 Bad Request."""
        exception_class = transform_http_status_to_exception(400)

        assert exception_class == ValidationError

    def test_transform_http_status_401(self):
        """Test transforming 401 Unauthorized."""
        exception_class = transform_http_status_to_exception(401)

        assert exception_class == AuthError

    def test_transform_http_status_403(self):
        """Test transforming 403 Forbidden."""
        exception_class = transform_http_status_to_exception(403)

        assert exception_class == AuthError

    def test_transform_http_status_404(self):
        """Test transforming 404 Not Found."""
        exception_class = transform_http_status_to_exception(404)

        assert exception_class == NotFoundError

    def test_transform_http_status_429(self):
        """Test transforming 429 Rate Limit."""
        exception_class = transform_http_status_to_exception(429)

        assert exception_class == RateLimitError

    def test_transform_http_status_500(self):
        """Test transforming 500 Internal Server Error."""
        exception_class = transform_http_status_to_exception(500)

        assert exception_class == ServerError

    def test_transform_http_status_503(self):
        """Test transforming 503 Service Unavailable."""
        exception_class = transform_http_status_to_exception(503)

        assert exception_class == ServerError

    def test_transform_http_status_unknown(self):
        """Test transforming unknown status code."""
        exception_class = transform_http_status_to_exception(418)

        assert exception_class == HTTPError

    def test_sanitize_error_strips_paths(self):
        """Test sanitize removes file paths from errors."""
        error = Exception("/home/user/secrets/config.py: connection failed")

        result = sanitize_error(error, "Connection error")

        assert "/home/user" not in result["error"]
        assert result["error"] == "Connection error"

    def test_sanitize_error_strips_api_keys(self):
        """Test sanitize doesn't leak API keys."""
        error = Exception("Auth failed with key: sk-abc123xyz")

        result = sanitize_error(error, "Authentication failed")

        assert "sk-abc123xyz" not in result["error"]
        assert result["error"] == "Authentication failed"

    def test_sanitize_error_with_none_message(self):
        """Test sanitize handles None message."""
        error = ValueError("Some internal error")

        result = sanitize_error(error, None)

        assert "error" in result
        assert result["error"] != ""

    def test_sanitize_error_empty_custom_message(self):
        """Test sanitize with empty custom message."""
        error = RuntimeError("Internal details")

        result = sanitize_error(error, "")

        assert result["error"] != ""
        assert "Internal details" not in result["error"]
