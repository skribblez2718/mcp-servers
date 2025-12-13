"""Tests for exception hierarchy.

Tests custom exception types and their attributes.
"""

import pytest
from src.exceptions import (
    HTTPError,
    RateLimitError,
    AuthError,
    NotFoundError,
    ValidationError,
    ServerError
)


class TestExceptions:
    """Test custom exception hierarchy."""

    def test_http_error_base(self):
        """Test HTTPError base exception."""
        error = HTTPError(
            message="Test error",
            status_code=500,
            response={"error": "test"}
        )

        assert error.message == "Test error"
        assert error.status_code == 500
        assert error.response == {"error": "test"}
        assert str(error) == "Test error"

    def test_http_error_without_response(self):
        """Test HTTPError without response data."""
        error = HTTPError(message="Test error", status_code=500)

        assert error.message == "Test error"
        assert error.status_code == 500
        assert error.response is None

    def test_rate_limit_error(self):
        """Test RateLimitError with retry_after."""
        error = RateLimitError(
            message="Rate limited",
            retry_after=60
        )

        assert error.message == "Rate limited"
        assert error.status_code == 429
        assert error.retry_after == 60

    def test_rate_limit_error_default_retry(self):
        """Test RateLimitError with default retry_after."""
        error = RateLimitError(message="Rate limited")

        assert error.status_code == 429
        assert error.retry_after == 60  # Default

    def test_auth_error_401(self):
        """Test AuthError for 401 unauthorized."""
        error = AuthError(message="Unauthorized")

        assert error.message == "Unauthorized"
        assert error.status_code == 401

    def test_auth_error_403(self):
        """Test AuthError for 403 forbidden."""
        error = AuthError(message="Forbidden", status_code=403)

        assert error.message == "Forbidden"
        assert error.status_code == 403

    def test_not_found_error(self):
        """Test NotFoundError."""
        error = NotFoundError(message="Resource not found")

        assert error.message == "Resource not found"
        assert error.status_code == 404

    def test_validation_error(self):
        """Test ValidationError with errors list."""
        errors = [
            {"field": "limit", "message": "must be positive"}
        ]
        error = ValidationError(
            message="Validation failed",
            errors=errors
        )

        assert error.message == "Validation failed"
        assert error.status_code == 400
        assert error.errors == errors

    def test_validation_error_no_errors(self):
        """Test ValidationError without errors list."""
        error = ValidationError(message="Invalid input")

        assert error.message == "Invalid input"
        assert error.status_code == 400
        assert error.errors == []

    def test_server_error_500(self):
        """Test ServerError with default 500 status."""
        error = ServerError(message="Internal error")

        assert error.message == "Internal error"
        assert error.status_code == 500

    def test_server_error_custom_5xx(self):
        """Test ServerError with custom 5xx status."""
        error = ServerError(message="Service unavailable", status_code=503)

        assert error.message == "Service unavailable"
        assert error.status_code == 503

    def test_exception_inheritance(self):
        """Test exception inheritance hierarchy."""
        # All custom exceptions inherit from HTTPError
        assert issubclass(RateLimitError, HTTPError)
        assert issubclass(AuthError, HTTPError)
        assert issubclass(NotFoundError, HTTPError)
        assert issubclass(ValidationError, HTTPError)
        assert issubclass(ServerError, HTTPError)

        # HTTPError inherits from Exception
        assert issubclass(HTTPError, Exception)

    def test_exception_can_be_caught_as_base(self):
        """Test exceptions can be caught as HTTPError."""
        with pytest.raises(HTTPError):
            raise NotFoundError("Not found")

        with pytest.raises(HTTPError):
            raise RateLimitError("Rate limited")
