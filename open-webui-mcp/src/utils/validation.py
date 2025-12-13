"""Input validation utilities for tool parameters.

Provides validation functions for common parameter types to prevent
injection attacks and ensure data integrity.
"""

import re
from typing import Any
from src.exceptions import ValidationError


class ToolInputValidator:
    """Input validation for tool parameters."""

    @staticmethod
    def validate_id(value: str, field_name: str = "id") -> str:
        """Validate ID format (alphanumeric, underscore, hyphen).

        Args:
            value: ID value to validate
            field_name: Name of field for error messages

        Returns:
            Validated ID value

        Raises:
            ValidationError: If ID format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"Invalid {field_name}: must be string")

        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise ValidationError(
                f"Invalid {field_name}: must be alphanumeric with _ or -"
            )

        if len(value) > 255:
            raise ValidationError(
                f"Invalid {field_name}: too long (max 255 characters)"
            )

        return value

    @staticmethod
    def validate_pagination(limit: int, offset: int) -> tuple[int, int]:
        """Validate pagination parameters.

        Args:
            limit: Items per page
            offset: Offset in results

        Returns:
            Validated (limit, offset) tuple

        Raises:
            ValidationError: If parameters are invalid
        """
        if not isinstance(limit, int) or not isinstance(offset, int):
            raise ValidationError("limit and offset must be integers")

        if limit < 1 or limit > 1000:
            raise ValidationError("limit must be between 1 and 1000")

        if offset < 0:
            raise ValidationError("offset must be >= 0")

        return limit, offset

    @staticmethod
    def validate_string_length(
        value: str,
        field_name: str,
        min_length: int = 0,
        max_length: int = 10000
    ) -> str:
        """Validate string length.

        Args:
            value: String value
            field_name: Field name for errors
            min_length: Minimum length
            max_length: Maximum length

        Returns:
            Validated string

        Raises:
            ValidationError: If length invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be string")

        if len(value) < min_length:
            raise ValidationError(
                f"{field_name} too short (min {min_length})"
            )

        if len(value) > max_length:
            raise ValidationError(
                f"{field_name} too long (max {max_length})"
            )

        return value

    @staticmethod
    def validate_enum(
        value: str,
        allowed: list[str],
        field_name: str = "value"
    ) -> str:
        """Validate enum value.

        Args:
            value: Value to validate
            allowed: List of allowed values
            field_name: Field name for errors

        Returns:
            Validated value

        Raises:
            ValidationError: If value not in allowed list
        """
        if value not in allowed:
            raise ValidationError(
                f"{field_name} must be one of: {', '.join(allowed)}"
            )

        return value

    @staticmethod
    def sanitize_path_component(value: str) -> str:
        """Sanitize path component to prevent traversal attacks.

        Args:
            value: Path component

        Returns:
            Sanitized value

        Raises:
            ValidationError: If path traversal detected
        """
        if '..' in value or value.startswith(('/','.')):
            raise ValidationError(
                "Invalid path component: traversal not allowed"
            )

        return value

    @staticmethod
    def validate_email(value: str, field_name: str = "email") -> str:
        """Validate email format.

        Args:
            value: Email address to validate
            field_name: Field name for error messages

        Returns:
            Validated email value

        Raises:
            ValidationError: If email format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be string")

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValidationError(f"Invalid {field_name}: {value}")

        return value

    @staticmethod
    def validate_url(value: str, field_name: str = "url") -> str:
        """Validate URL format.

        Args:
            value: URL to validate
            field_name: Field name for error messages

        Returns:
            Validated URL value

        Raises:
            ValidationError: If URL format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be string")

        from urllib.parse import urlparse

        try:
            parsed = urlparse(value)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValidationError(f"Invalid {field_name}: {value}")
            if parsed.scheme not in ['http', 'https']:
                raise ValidationError(f"{field_name} must use http:// or https://")
        except Exception as e:
            raise ValidationError(f"Invalid {field_name}: {e}")

        return value

    @staticmethod
    def validate_uuid(value: str, field_name: str = "id") -> str:
        """Validate UUID format.

        Args:
            value: UUID string to validate
            field_name: Field name for error messages

        Returns:
            Validated UUID value

        Raises:
            ValidationError: If UUID format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be string")

        import uuid

        try:
            uuid.UUID(value)
            return value
        except ValueError:
            raise ValidationError(f"Invalid UUID for {field_name}: {value}")

    @staticmethod
    def validate_json_string(value: str, field_name: str = "json") -> str:
        """Validate JSON string format.

        Args:
            value: JSON string to validate
            field_name: Field name for error messages

        Returns:
            Validated JSON string

        Raises:
            ValidationError: If JSON format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be string")

        import json

        try:
            json.loads(value)
            return value
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON for {field_name}: {e}")
