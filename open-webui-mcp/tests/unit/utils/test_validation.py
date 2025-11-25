"""Tests for input validation utilities.

Tests validation functions for IDs, pagination, strings, enums, and path safety.
"""

import pytest
from src.utils.validation import ToolInputValidator
from src.exceptions import ValidationError


class TestToolInputValidator:
    """Test input validation methods."""

    # ID Validation Tests
    def test_validate_id_valid(self):
        """Test valid ID formats."""
        assert ToolInputValidator.validate_id("chat-123") == "chat-123"
        assert ToolInputValidator.validate_id("user_456") == "user_456"
        assert ToolInputValidator.validate_id("model-abc_123") == "model-abc_123"
        assert ToolInputValidator.validate_id("ABC123") == "ABC123"

    def test_validate_id_invalid_characters(self):
        """Test ID with invalid characters."""
        with pytest.raises(ValidationError, match="must be alphanumeric"):
            ToolInputValidator.validate_id("chat@123")

        with pytest.raises(ValidationError, match="must be alphanumeric"):
            ToolInputValidator.validate_id("user/456")

        with pytest.raises(ValidationError, match="must be alphanumeric"):
            ToolInputValidator.validate_id("model.abc")

    def test_validate_id_too_long(self):
        """Test ID exceeding max length."""
        long_id = "a" * 256
        with pytest.raises(ValidationError, match="too long"):
            ToolInputValidator.validate_id(long_id)

    def test_validate_id_not_string(self):
        """Test ID with non-string type."""
        with pytest.raises(ValidationError, match="must be string"):
            ToolInputValidator.validate_id(123)

    def test_validate_id_custom_field_name(self):
        """Test ID validation with custom field name."""
        with pytest.raises(ValidationError, match="Invalid chat_id"):
            ToolInputValidator.validate_id("invalid@", field_name="chat_id")

    # Pagination Validation Tests
    def test_validate_pagination_valid(self):
        """Test valid pagination parameters."""
        limit, offset = ToolInputValidator.validate_pagination(10, 0)
        assert limit == 10
        assert offset == 0

        limit, offset = ToolInputValidator.validate_pagination(1000, 500)
        assert limit == 1000
        assert offset == 500

    def test_validate_pagination_limit_too_small(self):
        """Test pagination with limit < 1."""
        with pytest.raises(ValidationError, match="between 1 and 1000"):
            ToolInputValidator.validate_pagination(0, 0)

    def test_validate_pagination_limit_too_large(self):
        """Test pagination with limit > 1000."""
        with pytest.raises(ValidationError, match="between 1 and 1000"):
            ToolInputValidator.validate_pagination(1001, 0)

    def test_validate_pagination_offset_negative(self):
        """Test pagination with negative offset."""
        with pytest.raises(ValidationError, match="offset must be >= 0"):
            ToolInputValidator.validate_pagination(10, -1)

    def test_validate_pagination_not_integers(self):
        """Test pagination with non-integer types."""
        with pytest.raises(ValidationError, match="must be integers"):
            ToolInputValidator.validate_pagination("10", 0)

        with pytest.raises(ValidationError, match="must be integers"):
            ToolInputValidator.validate_pagination(10, "0")

    def test_validate_pagination_edge_cases(self):
        """Test pagination edge cases."""
        # Minimum valid
        limit, offset = ToolInputValidator.validate_pagination(1, 0)
        assert limit == 1
        assert offset == 0

        # Maximum valid
        limit, offset = ToolInputValidator.validate_pagination(1000, 999999)
        assert limit == 1000
        assert offset == 999999

    # String Length Validation Tests
    def test_validate_string_length_valid(self):
        """Test valid string lengths."""
        result = ToolInputValidator.validate_string_length(
            "test",
            "field",
            min_length=1,
            max_length=10
        )
        assert result == "test"

    def test_validate_string_length_too_short(self):
        """Test string too short."""
        with pytest.raises(ValidationError, match="too short"):
            ToolInputValidator.validate_string_length(
                "ab",
                "field",
                min_length=3
            )

    def test_validate_string_length_too_long(self):
        """Test string too long."""
        with pytest.raises(ValidationError, match="too long"):
            ToolInputValidator.validate_string_length(
                "a" * 101,
                "field",
                max_length=100
            )

    def test_validate_string_length_not_string(self):
        """Test non-string input."""
        with pytest.raises(ValidationError, match="must be string"):
            ToolInputValidator.validate_string_length(123, "field")

    # Enum Validation Tests
    def test_validate_enum_valid(self):
        """Test valid enum values."""
        allowed = ["active", "archived", "deleted"]
        result = ToolInputValidator.validate_enum("active", allowed, "status")
        assert result == "active"

    def test_validate_enum_invalid(self):
        """Test invalid enum value."""
        allowed = ["active", "archived"]
        with pytest.raises(ValidationError, match="must be one of"):
            ToolInputValidator.validate_enum("deleted", allowed, "status")

    def test_validate_enum_case_sensitive(self):
        """Test enum validation is case-sensitive."""
        allowed = ["active", "archived"]
        with pytest.raises(ValidationError):
            ToolInputValidator.validate_enum("Active", allowed)

    # Path Sanitization Tests
    def test_sanitize_path_component_valid(self):
        """Test valid path components."""
        assert ToolInputValidator.sanitize_path_component("file") == "file"
        assert ToolInputValidator.sanitize_path_component("test-123") == "test-123"

    def test_sanitize_path_component_traversal(self):
        """Test path traversal prevention."""
        with pytest.raises(ValidationError, match="traversal not allowed"):
            ToolInputValidator.sanitize_path_component("../etc")

        with pytest.raises(ValidationError, match="traversal not allowed"):
            ToolInputValidator.sanitize_path_component("file/../root")

    def test_sanitize_path_component_absolute(self):
        """Test absolute path prevention."""
        with pytest.raises(ValidationError, match="traversal not allowed"):
            ToolInputValidator.sanitize_path_component("/etc/passwd")

    def test_sanitize_path_component_hidden(self):
        """Test hidden file prevention."""
        with pytest.raises(ValidationError, match="traversal not allowed"):
            ToolInputValidator.sanitize_path_component(".hidden")
