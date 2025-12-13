"""Open WebUI MCP Server.

Main entry point for the MCP server providing tools for Open WebUI API.
Runs as HTTP server using Starlette and Uvicorn for production deployment.
"""

import json

import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response
from src.tools.factory import ToolFactory
from src.config import Config
from src.utils.logging_utils import setup_logging, get_logger
from src.utils.error_handler import sanitize_error

# Initialize configuration
config = Config()

# Setup logging
setup_logging(config.LOG_LEVEL, config.LOG_FORMAT)
logger = get_logger(__name__)

# Initialize tool factory
factory = ToolFactory(config)

# Create MCP server
mcp_server = Server("open-webui-mcp")


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools.

    Returns:
        List of Tool objects for MCP SDK
    """
    logger.info("Listing all tools")

    try:
        tools = factory.get_all_tools()
        tool_objects = []

        for tool in tools:
            definition = tool.get_definition()
            # Convert dict definition to mcp.types.Tool object
            tool_obj = Tool(
                name=definition["name"],
                description=definition.get("description"),
                inputSchema=definition.get("inputSchema", {"type": "object", "properties": {}})
            )
            tool_objects.append(tool_obj)

        logger.info(f"Registered {len(tool_objects)} tools")

        return tool_objects

    except Exception as e:
        logger.error(f"Failed to list tools: {e}", exc_info=True)
        # Return empty list on error
        return []


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> dict:
    """Execute an MCP tool.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        Tool execution result or error
    """
    logger.info(f"Calling tool: {name}", extra={"arguments": arguments})

    try:
        # Create or retrieve tool
        tool = factory.create_tool(name)

        # Execute tool
        result = await tool.execute(arguments)

        # Return MCP response
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }

    except Exception as e:
        # Sanitize error for client
        error_data = sanitize_error(e, f"Tool execution failed: {name}")

        logger.error(
            f"Tool {name} failed: {error_data['error']}",
            extra={"error_type": error_data['type']}
        )

        # Return MCP error response
        return {
            "isError": True,
            "content": [
                {
                    "type": "text",
                    "text": error_data["error"]
                }
            ]
        }


# Create SSE transport
sse = SseServerTransport("/messages")


async def handle_sse(request: Request) -> Response:
    """Handle SSE connection requests.

    Args:
        request: Starlette request object

    Returns:
        SSE response stream
    """
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send,
    ) as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options(),
        )
    return Response()


async def handle_messages(request: Request) -> Response:
    """Handle MCP message posts.

    Args:
        request: Starlette request object

    Returns:
        Empty response
    """
    await sse.handle_post_message(request.scope, request.receive, request._send)
    return Response()


# Create Starlette app with MCP routes
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ],
)


def main() -> None:
    """Run the HTTP MCP server using uvicorn."""
    logger.info("Starting Open WebUI MCP Server (HTTP Mode)")
    logger.info(f"Base URL: {config.OPENWEBUI_BASE_URL}")
    logger.info(f"Rate Limit: {config.OPENWEBUI_RATE_LIMIT} req/s")
    logger.info(f"Listening on http://{config.HOST}:{config.PORT}")

    try:
        uvicorn.run(
            app,
            host=config.HOST,
            port=config.PORT,
            log_level=config.LOG_LEVEL.lower(),
        )
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise
    finally:
        logger.info("Server shutdown complete")


if __name__ == "__main__":
    main()
