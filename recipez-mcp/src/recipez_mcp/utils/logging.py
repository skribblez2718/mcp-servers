"""Structured JSON logging configuration for Recipez MCP server.

Provides centralized logging with structured JSON output for easy parsing
and integration with log aggregation systems.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class StructuredJSONFormatter(logging.Formatter):
    """JSON formatter for structured logging.

    Outputs log records as JSON objects with consistent schema:
    {
        "timestamp": "ISO 8601 timestamp",
        "level": "DEBUG|INFO|WARN|ERROR",
        "message": "Human-readable message",
        "context": {
            "tool_name": "...",
            "endpoint": "...",
            "request_id": "...",
            "duration_ms": 123,
            ...
        }
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON string
        """
        # Base log structure
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Extract context from record extras
        context = {}
        for key, value in record.__dict__.items():
            # Skip standard logging attributes
            if key not in [
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
            ]:
                context[key] = value

        # Add context if present
        if context:
            log_data["context"] = context

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Get or create a structured JSON logger.

    Args:
        name: Logger name (typically module name)
        level: Log level (DEBUG|INFO|WARN|ERROR)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        # JSON formatter for structured output
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJSONFormatter())
        logger.addHandler(handler)

        # Prevent propagation to root logger
        logger.propagate = False

    return logger


def log_tool_execution(
    logger: logging.Logger,
    tool_name: str,
    operation: Optional[str] = None,
    duration_ms: Optional[int] = None,
    status: str = "success",
    **kwargs: Any,
) -> None:
    """Log tool execution event with structured context.

    Args:
        logger: Logger instance
        tool_name: Name of the tool being executed
        operation: Specific operation within tool (e.g., "create", "read")
        duration_ms: Execution duration in milliseconds
        status: Execution status (success|error)
        **kwargs: Additional context fields
    """
    context = {
        "tool_name": tool_name,
        "status": status,
    }

    if operation:
        context["operation"] = operation
    if duration_ms is not None:
        context["duration_ms"] = duration_ms

    # Merge additional context
    context.update(kwargs)

    message = f"Tool execution: {tool_name}"
    if operation:
        message += f" ({operation})"

    logger.info(message, extra=context)


def log_api_call(
    logger: logging.Logger,
    method: str,
    endpoint: str,
    status_code: Optional[int] = None,
    duration_ms: Optional[int] = None,
    **kwargs: Any,
) -> None:
    """Log API call event with structured context.

    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        status_code: HTTP response status code
        duration_ms: Request duration in milliseconds
        **kwargs: Additional context fields
    """
    context = {
        "method": method,
        "endpoint": endpoint,
    }

    if status_code is not None:
        context["status_code"] = status_code
    if duration_ms is not None:
        context["duration_ms"] = duration_ms

    # Merge additional context
    context.update(kwargs)

    message = f"API call: {method} {endpoint}"
    if status_code:
        message += f" [{status_code}]"

    level = logging.INFO if status_code and status_code < 400 else logging.ERROR
    logger.log(level, message, extra=context)


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    message: str,
    severity: str = "info",
    **kwargs: Any,
) -> None:
    """Log security-related event.

    Args:
        logger: Logger instance
        event_type: Type of security event (auth_success, auth_failure, token_refresh, etc.)
        message: Event description
        severity: Event severity (info|warning|error|critical)
        **kwargs: Additional context fields
    """
    context = {
        "event_type": event_type,
        "security_event": True,
    }

    # Merge additional context
    context.update(kwargs)

    level_map = {
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    logger.log(level_map.get(severity, logging.INFO), message, extra=context)


# Module-level logger for this utilities package
logger = get_logger(__name__)
