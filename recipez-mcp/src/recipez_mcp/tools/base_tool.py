"""Abstract base class for all MCP tools.

Defines the interface that all Recipez MCP tools must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from recipez_mcp.client.http_client import HTTPClient
from recipez_mcp.utils.logging import get_logger


class BaseTool(ABC):
    """Abstract base class for MCP tools.

    All tools must implement:
    - name(): Return tool name
    - description(): Return tool description
    - input_schema(): Return JSON schema for tool parameters
    - execute(): Perform the tool's operation
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize tool with HTTP client dependency.

        Args:
            http_client: HTTPClient instance for making API requests
        """
        self.http_client = http_client
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def name(self) -> str:
        """Return the tool name (e.g., 'recipez_health_check').

        Returns:
            Tool name string
        """
        pass

    @abstractmethod
    def description(self) -> str:
        """Return human-readable tool description.

        Returns:
            Tool description string
        """
        pass

    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """Return JSON schema defining tool parameters.

        Returns:
            JSON schema dict with type, properties, required fields
        """
        pass

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool's operation with given parameters.

        Args:
            params: Dictionary of parameter values matching input_schema

        Returns:
            Dictionary of result data

        Raises:
            MCPError: On validation or API errors
        """
        pass
