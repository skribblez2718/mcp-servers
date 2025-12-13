"""Utility functions and classes for Recipez MCP server.

Provides reusable components for validation, error handling, and logging.
"""

from recipez_mcp.utils.errors import (
    MCPAuthError,
    MCPConflictError,
    MCPError,
    MCPForbiddenError,
    MCPInternalError,
    MCPNotFoundError,
    MCPRateLimitError,
    MCPTimeoutError,
    MCPValidationError,
    map_http_status_to_error,
)
from recipez_mcp.utils.logging import (
    StructuredJSONFormatter,
    get_logger,
    log_api_call,
    log_security_event,
    log_tool_execution,
    logger,
)
from recipez_mcp.utils.validation import (
    MeasurementUnit,
    QUANTITY_PATTERN,
    validate_category_name,
    validate_email,
    validate_ingredient_name,
    validate_measurement,
    validate_quantity,
    validate_recipe_name,
    validate_url,
    validate_uuid,
)

__all__ = [
    # Errors
    "MCPAuthError",
    "MCPConflictError",
    "MCPError",
    "MCPForbiddenError",
    "MCPInternalError",
    "MCPNotFoundError",
    "MCPRateLimitError",
    "MCPTimeoutError",
    "MCPValidationError",
    "map_http_status_to_error",
    # Logging
    "StructuredJSONFormatter",
    "get_logger",
    "log_api_call",
    "log_security_event",
    "log_tool_execution",
    "logger",
    # Validation
    "MeasurementUnit",
    "QUANTITY_PATTERN",
    "validate_category_name",
    "validate_email",
    "validate_ingredient_name",
    "validate_measurement",
    "validate_quantity",
    "validate_recipe_name",
    "validate_url",
    "validate_uuid",
]
