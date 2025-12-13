"""Tool factory with decorator-based registration and dependency injection.

Provides centralized tool management with automatic HTTPClient injection.
"""

from typing import Dict, Type

from recipez_mcp.client.http_client import HTTPClient
from recipez_mcp.tools.base_tool import BaseTool
from recipez_mcp.utils.logging import get_logger

# Import all tools for registration
from recipez_mcp.tools.ai import AITool
from recipez_mcp.tools.api_keys import ApiKeysManageTool
from recipez_mcp.tools.categories import CategoriesTool
from recipez_mcp.tools.email import EmailTool
from recipez_mcp.tools.grocery import GroceryTool
from recipez_mcp.tools.health import HealthCheckTool
from recipez_mcp.tools.images import ImagesTool
from recipez_mcp.tools.ingredients import IngredientsTool
from recipez_mcp.tools.profile import ProfileGetTool, ProfileUpdateImageTool
from recipez_mcp.tools.recipes import RecipesTool
from recipez_mcp.tools.steps import StepsTool


logger = get_logger("ToolFactory")


class ToolFactory:
    """Factory for creating and managing MCP tools.

    Provides:
    - Tool registration and discovery
    - Dependency injection (HTTPClient, config)
    - Singleton HTTP client management
    """

    _registry: Dict[str, Type[BaseTool]] = {}
    _http_client: HTTPClient | None = None

    @classmethod
    def register_tool(cls, tool_class: Type[BaseTool]) -> Type[BaseTool]:
        """Register a tool class in the factory.

        Args:
            tool_class: Tool class to register

        Returns:
            The same tool class (for decorator chaining)
        """
        # Instantiate temporarily to get the tool name
        temp_instance = tool_class(cls._get_http_client())
        tool_name = temp_instance.name()
        cls._registry[tool_name] = tool_class
        logger.info(f"Registered tool: {tool_name}")
        return tool_class

    @classmethod
    def get_tool(cls, name: str) -> BaseTool:
        """Get a tool instance by name.

        Args:
            name: Tool name (e.g., 'recipez_health_check')

        Returns:
            Tool instance with injected dependencies

        Raises:
            KeyError: If tool not found
        """
        tool_class = cls._registry.get(name)
        if not tool_class:
            raise KeyError(f"Tool '{name}' not found in registry")

        http_client = cls._get_http_client()
        return tool_class(http_client)

    @classmethod
    def list_tools(cls) -> list[str]:
        """List all registered tool names.

        Returns:
            List of tool names
        """
        return list(cls._registry.keys())

    @classmethod
    def _get_http_client(cls) -> HTTPClient:
        """Get singleton HTTPClient instance.

        Returns:
            HTTPClient instance
        """
        if cls._http_client is None:
            cls._http_client = HTTPClient()
        return cls._http_client

    @classmethod
    def reset(cls) -> None:
        """Reset factory state (for testing).

        Clears registry and HTTP client singleton.
        """
        cls._registry.clear()
        cls._http_client = None


# Register all tools
ToolFactory.register_tool(HealthCheckTool)
ToolFactory.register_tool(ProfileGetTool)
ToolFactory.register_tool(ProfileUpdateImageTool)
ToolFactory.register_tool(ApiKeysManageTool)
ToolFactory.register_tool(RecipesTool)
ToolFactory.register_tool(CategoriesTool)
ToolFactory.register_tool(IngredientsTool)
ToolFactory.register_tool(StepsTool)
ToolFactory.register_tool(ImagesTool)
ToolFactory.register_tool(AITool)
ToolFactory.register_tool(GroceryTool)
ToolFactory.register_tool(EmailTool)

logger.info(f"ToolFactory initialized with {len(ToolFactory.list_tools())} tools")
