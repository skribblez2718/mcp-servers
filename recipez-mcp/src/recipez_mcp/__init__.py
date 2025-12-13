"""Recipez MCP Server - Model Context Protocol server for Recipez API.

Provides MCP tools for recipe management, AI recipe generation, grocery lists,
and email operations through the Recipez REST API.
"""

__version__ = "0.1.0"
__author__ = "Recipez Team"
__description__ = "MCP server for Recipez recipe management API"

# Export key components for external use
from recipez_mcp.config.settings import Settings, get_settings
from recipez_mcp.factory import ToolFactory
from recipez_mcp.server import app

__all__ = [
    "__version__",
    "__author__",
    "__description__",
    "Settings",
    "get_settings",
    "ToolFactory",
    "app",
]
