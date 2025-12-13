"""Base tool class for all MCP tools.

Provides common functionality for tool execution and validation.
"""

from typing import Any, Protocol
from abc import abstractmethod
import logging
import time
from src.services.client import OpenWebUIClient
from src.config import Config

logger = logging.getLogger(__name__)


class MCPTool(Protocol):
    """Protocol that all MCP tools must implement.

    This defines the interface for tool discovery and execution.
    """

    @abstractmethod
    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition dict with name, description, and inputSchema
        """
        ...

    @abstractmethod
    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute the tool.

        Args:
            arguments: Tool arguments from MCP client

        Returns:
            Tool execution result

        Raises:
            ValidationError: If arguments are invalid
            HTTPError: If API call fails
        """
        ...


class BaseTool:
    """Base class for all Open WebUI MCP tools.

    Provides common functionality for API communication and validation.

    Args:
        client: OpenWebUI HTTP client
        config: Configuration instance
    """

    def __init__(self, client: OpenWebUIClient, config: Config) -> None:
        """Initialize base tool.

        Args:
            client: HTTP client instance
            config: Configuration instance
        """
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition dict

        Note:
            Must be implemented by subclasses
        """
        raise NotImplementedError

    @abstractmethod
    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute the tool.

        Args:
            arguments: Tool arguments

        Returns:
            Execution result

        Note:
            Must be implemented by subclasses
        """
        raise NotImplementedError

    def _log_execution_start(self, arguments: dict[str, Any]) -> None:
        """Log tool execution start and store start time.

        Args:
            arguments: Tool arguments
        """
        self._start_time = time.time()
        # Sanitize arguments for logging (hide sensitive data)
        safe_args = self._sanitize_args_for_logging(arguments)
        self.logger.info(
            f"Executing {self.__class__.__name__}",
            extra={"arguments": safe_args, "tool_name": self.__class__.__name__}
        )

    def _log_execution_end(self, result: dict[str, Any] | list) -> None:
        """Log tool execution end with timing.

        Args:
            result: Execution result (dict or list)
        """
        duration_ms = (time.time() - getattr(self, '_start_time', time.time())) * 1000
        result_preview = self._get_result_preview(result)
        self.logger.info(
            f"Completed {self.__class__.__name__} in {duration_ms:.0f}ms",
            extra={
                "tool_name": self.__class__.__name__,
                "duration_ms": duration_ms,
                "result_keys": list(result.keys()) if isinstance(result, dict) else f"[{len(result)} items]",
                "result_preview": result_preview
            }
        )

    def _log_execution_error(self, error: Exception) -> None:
        """Log tool execution error with details.

        Args:
            error: The exception that occurred
        """
        duration_ms = (time.time() - getattr(self, '_start_time', time.time())) * 1000
        self.logger.error(
            f"Failed {self.__class__.__name__} after {duration_ms:.0f}ms: {type(error).__name__}: {error}",
            extra={
                "tool_name": self.__class__.__name__,
                "duration_ms": duration_ms,
                "error_type": type(error).__name__,
                "error_message": str(error)
            },
            exc_info=True
        )

    def _sanitize_args_for_logging(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Sanitize arguments for logging (hide sensitive data).

        Args:
            arguments: Raw arguments

        Returns:
            Sanitized arguments safe for logging
        """
        sensitive_keys = {'password', 'token', 'api_key', 'secret', 'auth'}
        sanitized = {}
        for key, value in arguments.items():
            if any(s in key.lower() for s in sensitive_keys):
                sanitized[key] = '***REDACTED***'
            elif isinstance(value, str) and len(value) > 200:
                sanitized[key] = f"{value[:200]}... (truncated)"
            else:
                sanitized[key] = value
        return sanitized

    def _get_result_preview(self, result: dict[str, Any] | list) -> str:
        """Get a preview of the result for logging.

        Args:
            result: Execution result (dict or list)

        Returns:
            String preview of result
        """
        if not result:
            return "(empty)"
        # Handle list responses (common for collection endpoints)
        if isinstance(result, list):
            return f"[{len(result)} items]"
        # Handle dict responses
        if isinstance(result, dict):
            if 'data' in result and isinstance(result['data'], list):
                return f"{{data: [{len(result['data'])} items]}}"
            return f"{{keys: {list(result.keys())[:5]}}}"
        return str(type(result).__name__)
