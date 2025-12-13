"""Reusable validation utilities for Recipez MCP server.

Provides validators for common patterns (UUIDs, measurements, quantities, etc.)
used across models and tools.
"""

import re
from enum import Enum
from uuid import UUID


class MeasurementUnit(str, Enum):
    """Allowed measurement units for ingredients.

    Based on OpenAPI MeasurementEnum specification.
    """

    # Weight
    GRAM = "gram"
    OUNCE = "ounce"
    POUND = "pound"
    KILOGRAM = "kilogram"

    # Volume
    TEASPOON = "teaspoon"
    TABLESPOON = "tablespoon"
    FLUID_OUNCE = "fluid ounce"
    CUP = "cup"
    PINT = "pint"
    QUART = "quart"
    GALLON = "gallon"
    MILLILITER = "milliliter"
    LITER = "liter"

    # Abbreviations
    TSP = "tsp"
    TBSP = "Tbsp"

    # Approximate
    PINCH = "pinch"
    DASH = "dash"
    DOLLOP = "dollop"
    HANDFUL = "handful"

    # Item-based
    CLOVE = "clove"
    SPRIG = "sprig"
    PIECE = "piece"
    SLICE = "slice"
    WHOLE = "whole"


# Quantity pattern: Numeric value, fraction, or range
# Examples: "1", "1.5", "1/2", "1-2", "1.5-2", "1/2-3/4"
QUANTITY_PATTERN = re.compile(
    r"^(\d+(\.\d+)?|\d+/\d+)(\s*-\s*(\d+(\.\d+)?|\d+/\d+))?$"
)


def validate_uuid(value: str) -> UUID:
    """Validate and parse UUID string.

    Args:
        value: UUID string to validate

    Returns:
        UUID object

    Raises:
        ValueError: If string is not valid UUID format
    """
    try:
        return UUID(value)
    except ValueError as e:
        raise ValueError(f"Invalid UUID format: {value}") from e


def validate_quantity(value: str) -> bool:
    """Validate ingredient quantity format.

    Accepts: decimals, fractions, ranges
    Examples: "1", "1.5", "1/2", "1-2", "1.5-2.5"

    Args:
        value: Quantity string to validate

    Returns:
        True if valid format

    Raises:
        ValueError: If format is invalid
    """
    if not QUANTITY_PATTERN.match(value):
        raise ValueError(
            f"Invalid quantity format: {value}. "
            "Must be numeric, fraction, or range (e.g., '1', '1.5', '1/2', '1-2')"
        )
    return True


def validate_measurement(value: str) -> bool:
    """Validate measurement unit.

    Args:
        value: Measurement unit string

    Returns:
        True if valid measurement unit

    Raises:
        ValueError: If not a valid measurement unit
    """
    valid_units = {unit.value for unit in MeasurementUnit}
    if value not in valid_units:
        raise ValueError(
            f"Invalid measurement unit: {value}. "
            f"Must be one of: {', '.join(sorted(valid_units))}"
        )
    return True


def validate_email(value: str) -> bool:
    """Validate email address format (basic validation).

    Args:
        value: Email address string

    Returns:
        True if valid format

    Raises:
        ValueError: If format is invalid
    """
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not email_pattern.match(value):
        raise ValueError(f"Invalid email format: {value}")
    return True


def validate_url(value: str) -> bool:
    """Validate URL format (basic validation).

    Args:
        value: URL string

    Returns:
        True if valid format

    Raises:
        ValueError: If format is invalid
    """
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    if not url_pattern.match(value):
        raise ValueError(f"Invalid URL format: {value}")
    return True


def validate_recipe_name(value: str) -> bool:
    """Validate recipe name format.

    Per OpenAPI: ^[0-9a-zA-Z-_()., '&]+$ (2-50 chars)

    Args:
        value: Recipe name string

    Returns:
        True if valid format

    Raises:
        ValueError: If format is invalid
    """
    if not 2 <= len(value) <= 50:
        raise ValueError(f"Recipe name must be 2-50 characters, got {len(value)}")

    pattern = re.compile(r"^[0-9a-zA-Z-_()., '&]+$")
    if not pattern.match(value):
        raise ValueError(
            f"Recipe name contains invalid characters: {value}. "
            "Allowed: alphanumeric, -, _, (), ., comma, space, ', &"
        )
    return True


def validate_category_name(value: str) -> bool:
    """Validate category name format.

    Per OpenAPI: ^[a-zA-Z0-9-_' ]+$ (2-50 chars)

    Args:
        value: Category name string

    Returns:
        True if valid format

    Raises:
        ValueError: If format is invalid
    """
    if not 2 <= len(value) <= 50:
        raise ValueError(f"Category name must be 2-50 characters, got {len(value)}")

    pattern = re.compile(r"^[a-zA-Z0-9-_' ]+$")
    if not pattern.match(value):
        raise ValueError(
            f"Category name contains invalid characters: {value}. "
            "Allowed: alphanumeric, -, _, ', space"
        )
    return True


def validate_ingredient_name(value: str) -> bool:
    """Validate ingredient name format.

    Per OpenAPI: ^[a-zA-Z0-9\\s()\\-°]+$ (2-50 chars)

    Args:
        value: Ingredient name string

    Returns:
        True if valid format

    Raises:
        ValueError: If format is invalid
    """
    if not 2 <= len(value) <= 50:
        raise ValueError(f"Ingredient name must be 2-50 characters, got {len(value)}")

    pattern = re.compile(r"^[a-zA-Z0-9\s()\-°]+$")
    if not pattern.match(value):
        raise ValueError(
            f"Ingredient name contains invalid characters: {value}. "
            "Allowed: alphanumeric, space, (), -, °"
        )
    return True
