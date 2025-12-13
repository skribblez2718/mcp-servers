"""CLI entry point for running the Recipez MCP server.

Usage:
    python -m recipez_mcp
    uv run python -m recipez_mcp
"""

import sys

import uvicorn

from recipez_mcp.config.settings import get_settings
from recipez_mcp.utils.logging import get_logger

logger = get_logger("main")


def main() -> None:
    """Run the MCP server using uvicorn."""
    try:
        settings = get_settings()
        logger.info(f"Starting Recipez MCP server on {settings.host}:{settings.port}")
        logger.info(f"Log level: {settings.log_level}")
        logger.info(f"Recipez API URL: {settings.recipez_base_url}")

        uvicorn.run(
            "recipez_mcp.server:app",
            host=settings.host,
            port=settings.port,
            log_level=settings.log_level.lower(),
            reload=False,
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
