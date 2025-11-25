"""Tool factory with dependency injection and lazy loading.

Manages tool instantiation, caching, and dependency injection for all MCP tools.
"""

import logging
import importlib
import pkgutil
from typing import Any
from pathlib import Path
from src.config import Config
from src.services.client import OpenWebUIClient
from src.utils.rate_limiter import RateLimiter
from src.tools.base import MCPTool

logger = logging.getLogger(__name__)


class ToolFactory:
    """Factory for creating MCP tool instances with dependency injection.

    Provides lazy loading, caching, and automatic tool discovery.

    Args:
        config: Configuration instance
    """

    def __init__(self, config: Config) -> None:
        """Initialize tool factory.

        Args:
            config: Configuration instance
        """
        self.config = config
        self._client: OpenWebUIClient | None = None
        self._services: dict[str, Any] = {}
        self._tools_cache: dict[str, MCPTool] = {}

    @property
    def client(self) -> OpenWebUIClient:
        """Get or create HTTP client.

        Returns:
            OpenWebUI HTTP client instance
        """
        if self._client is None:
            rate_limiter = self.get_service('rate_limiter')
            self._client = OpenWebUIClient(
                config=self.config,
                rate_limiter=rate_limiter
            )

        return self._client

    def get_service(self, name: str) -> Any:
        """Get or create a service.

        Args:
            name: Service name

        Returns:
            Service instance
        """
        if name not in self._services:
            if name == 'rate_limiter':
                self._services[name] = RateLimiter(
                    rate=self.config.OPENWEBUI_RATE_LIMIT
                )
            else:
                raise ValueError(f"Unknown service: {name}")

        return self._services[name]

    def create_tool(self, name: str) -> MCPTool:
        """Create or retrieve cached tool instance.

        Args:
            name: Tool name (e.g., "chat_list", "model_get")

        Returns:
            Tool instance

        Raises:
            ValueError: If tool not found
        """
        # Check cache
        if name in self._tools_cache:
            logger.debug(f"Tool {name} retrieved from cache")
            return self._tools_cache[name]

        logger.info(f"Creating tool: {name}")

        # Resolve module path and class name
        module_path, class_name = self._resolve_tool(name)

        # Import tool class
        try:
            tool_class = self._import_tool_class(module_path, class_name)
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to import tool {name}: {e}")
            raise ValueError(f"Tool not found: {name}") from e

        # Instantiate with dependencies
        tool_instance = tool_class(
            client=self.client,
            config=self.config
        )

        # Cache instance
        self._tools_cache[name] = tool_instance

        return tool_instance

    def get_all_tools(self) -> list[MCPTool]:
        """Discover and return all available tools.

        Returns:
            List of all tool instances
        """
        tool_names = self._discover_tools()
        logger.info(f"Discovered {len(tool_names)} tools")

        tools: list[MCPTool] = []
        for name in tool_names:
            try:
                tool = self.create_tool(name)
                tools.append(tool)
            except Exception as e:
                logger.warning(f"Failed to load tool {name}: {e}")
                continue

        return tools

    def _discover_tools(self) -> list[str]:
        """Scan tools directory and discover available tools.

        Returns:
            List of tool names
        """
        tool_names: list[str] = []

        # Get tools directory
        tools_dir = Path(__file__).parent

        # Scan subdirectories for tool modules
        for subdir in tools_dir.iterdir():
            if not subdir.is_dir() or subdir.name.startswith('_'):
                continue

            # Scan for *_tool.py files
            for tool_file in subdir.glob("*_tool.py"):
                # Extract tool name
                tool_name = tool_file.stem
                tool_names.append(tool_name)

        return sorted(tool_names)

    def _resolve_tool(self, name: str) -> tuple[str, str]:
        """Resolve tool name to module path and class name.

        Args:
            name: Tool name (e.g., "chat_list_tool")

        Returns:
            Tuple of (module_path, class_name)
        """
        # Remove _tool suffix if present
        if name.endswith('_tool'):
            base_name = name
        else:
            base_name = f"{name}_tool"

        # Infer resource group from name
        parts = base_name.split('_')
        if len(parts) >= 2:
            resource = parts[0]
        else:
            resource = 'misc'

        # Build module path
        # Example: chat_list_tool -> tools.chats.chat_list_tool
        module_path = f"src.tools.{resource}s.{base_name}"

        # Build class name (CamelCase)
        # Example: chat_list_tool -> ChatListTool
        words = base_name.replace('_tool', '').split('_')
        class_name = ''.join(word.capitalize() for word in words) + 'Tool'

        return module_path, class_name

    def _import_tool_class(self, module_path: str, class_name: str) -> type:
        """Dynamically import tool class.

        Args:
            module_path: Python module path
            class_name: Class name

        Returns:
            Tool class

        Raises:
            ImportError: If module not found
            AttributeError: If class not found
        """
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self._client:
            await self._client.close()
            self._client = None

        self._tools_cache.clear()
        self._services.clear()
