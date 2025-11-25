"""Base tool class for all MCP tools.

Provides common functionality for tool execution and validation.
"""

from typing import Any, Protocol
from abc import abstractmethod
import logging
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
        """Log tool execution start.

        Args:
            arguments: Tool arguments
        """
        self.logger.info(
            f"Executing {self.__class__.__name__}",
            extra={"arguments": arguments}
        )

    def _log_execution_end(self, result: dict[str, Any]) -> None:
        """Log tool execution end.

        Args:
            result: Execution result
        """
        self.logger.info(
            f"Completed {self.__class__.__name__}",
            extra={"result_keys": list(result.keys())}
        )
