"""Custom exception hierarchy for Recipez MCP server.

Provides MCP-specific exceptions that map to HTTP status codes
and MCP error response formats.
"""


class MCPError(Exception):
    """Base exception for MCP-related errors."""

    def __init__(self, message: str, http_status: int = 500):
        """Initialize MCP error.

        Args:
            message: Human-readable error message
            http_status: Associated HTTP status code
        """
        super().__init__(message)
        self.message = message
        self.http_status = http_status


class MCPAuthError(MCPError):
    """Authentication error (HTTP 401).

    Raised when JWT token is missing, invalid, or expired.
    """

    def __init__(self, message: str = "Invalid or expired JWT token"):
        """Initialize authentication error.

        Args:
            message: Error message (default: invalid/expired token)
        """
        super().__init__(message, http_status=401)


class MCPForbiddenError(MCPError):
    """Authorization error (HTTP 403).

    Raised when authenticated user lacks required scopes or permissions.
    """

    def __init__(self, message: str = "Insufficient permissions"):
        """Initialize forbidden error.

        Args:
            message: Error message (default: insufficient permissions)
        """
        super().__init__(message, http_status=403)


class MCPNotFoundError(MCPError):
    """Resource not found error (HTTP 404).

    Raised when requested resource does not exist.
    """

    def __init__(self, message: str = "Resource not found"):
        """Initialize not found error.

        Args:
            message: Error message (default: resource not found)
        """
        super().__init__(message, http_status=404)


class MCPValidationError(MCPError):
    """Validation error (HTTP 400).

    Raised when request parameters fail validation.
    """

    def __init__(self, message: str = "Invalid request parameters"):
        """Initialize validation error.

        Args:
            message: Error message (default: invalid parameters)
        """
        super().__init__(message, http_status=400)


class MCPRateLimitError(MCPError):
    """Rate limit exceeded error (HTTP 429).

    Raised when API rate limit is exceeded.
    """

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 0):
        """Initialize rate limit error.

        Args:
            message: Error message (default: rate limit exceeded)
            retry_after: Seconds until rate limit resets
        """
        super().__init__(message, http_status=429)
        self.retry_after = retry_after


class MCPInternalError(MCPError):
    """Internal server error (HTTP 500).

    Raised when API returns server error or unexpected condition occurs.
    """

    def __init__(self, message: str = "Internal server error"):
        """Initialize internal error.

        Args:
            message: Error message (default: internal server error)
        """
        super().__init__(message, http_status=500)


class MCPTimeoutError(MCPError):
    """Request timeout error (HTTP 504).

    Raised when API request times out.
    """

    def __init__(self, message: str = "Request timeout", timeout_seconds: int = 0):
        """Initialize timeout error.

        Args:
            message: Error message (default: request timeout)
            timeout_seconds: Timeout duration in seconds
        """
        super().__init__(message, http_status=504)
        self.timeout_seconds = timeout_seconds


class MCPConflictError(MCPError):
    """Conflict error (HTTP 409).

    Raised when request conflicts with existing resource (e.g., duplicate name).
    """

    def __init__(self, message: str = "Resource conflict"):
        """Initialize conflict error.

        Args:
            message: Error message (default: resource conflict)
        """
        super().__init__(message, http_status=409)


def map_http_status_to_error(status_code: int, message: str) -> MCPError:
    """Map HTTP status code to appropriate MCP exception.

    Args:
        status_code: HTTP status code
        message: Error message from API

    Returns:
        Appropriate MCPError subclass instance
    """
    error_map = {
        400: MCPValidationError,
        401: MCPAuthError,
        403: MCPForbiddenError,
        404: MCPNotFoundError,
        409: MCPConflictError,
        429: MCPRateLimitError,
        504: MCPTimeoutError,
    }

    # Get specific error class or default to MCPInternalError for 5xx
    error_class = error_map.get(status_code)
    if error_class:
        return error_class(message)

    if 500 <= status_code < 600:
        return MCPInternalError(message)

    # Fallback for unknown status codes
    return MCPError(message, http_status=status_code)
