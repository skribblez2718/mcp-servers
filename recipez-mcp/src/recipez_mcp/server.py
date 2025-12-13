"""MCP server with HTTP/SSE transport using Starlette and mcp library.

Provides SSE-based communication for MCP clients like Claude Desktop.
"""

import asyncio
import json
from typing import Any, Dict

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.routing import Route

from recipez_mcp.config.settings import get_settings
from recipez_mcp.factory import ToolFactory
from recipez_mcp.utils.errors import MCPError
from recipez_mcp.utils.logging import get_logger, log_tool_execution

logger = get_logger("MCPServer")

# Create MCP server instance
mcp_server = Server("recipez-mcp")


# Register all tools with MCP server
def register_tools() -> None:
    """Register all tools from ToolFactory with MCP server."""
    for tool_name in ToolFactory.list_tools():
        tool_instance = ToolFactory.get_tool(tool_name)

        @mcp_server.call_tool()
        async def handle_tool_call(
            name: str, arguments: Dict[str, Any]
        ) -> list[Any]:
            """Handle tool execution requests.

            Args:
                name: Tool name
                arguments: Tool parameters

            Returns:
                List of result content items
            """
            try:
                tool = ToolFactory.get_tool(name)
                result = await tool.execute(arguments)
                return [{"type": "text", "text": json.dumps(result, indent=2)}]
            except MCPError as e:
                logger.error(f"MCP error in tool '{name}': {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]
            except Exception as e:
                logger.error(f"Unexpected error in tool '{name}': {e}")
                return [
                    {
                        "type": "text",
                        "text": f"Internal error: {str(e)}",
                    }
                ]

        # Register tool metadata
        mcp_server.list_tools().append(
            {
                "name": tool_name,
                "description": tool_instance.description(),
                "inputSchema": tool_instance.input_schema(),
            }
        )

    logger.info(f"Registered {len(ToolFactory.list_tools())} tools with MCP server")


# SSE endpoint handler
async def sse_handler(request: Request) -> StreamingResponse:
    """Handle SSE connections from MCP clients.

    Args:
        request: Starlette request object

    Returns:
        StreamingResponse with SSE transport
    """
    logger.info("SSE connection established")

    async def event_stream() -> Any:
        """Generate SSE events."""
        transport = SseServerTransport("/messages")
        async with transport.connect_sse(request.scope, request.receive) as streams:
            await mcp_server.run(
                streams[0], streams[1], mcp_server.create_initialization_options()
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


# Messages endpoint handler
async def messages_handler(request: Request) -> Response:
    """Handle MCP messages from clients.

    Args:
        request: Starlette request object

    Returns:
        JSON response
    """
    try:
        data = await request.json()
        logger.debug(f"Received message: {data}")

        # MCP protocol handling would go here
        # For now, return success response
        return JSONResponse({"status": "ok"})
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# Health check endpoint
async def health_handler(request: Request) -> JSONResponse:
    """Health check endpoint for orchestration.

    Args:
        request: Starlette request object

    Returns:
        JSON response with health status
    """
    return JSONResponse(
        {
            "status": "healthy",
            "service": "recipez-mcp",
            "tools_registered": len(ToolFactory.list_tools()),
        }
    )


# Create Starlette app
def create_app() -> Starlette:
    """Create and configure Starlette ASGI application.

    Returns:
        Configured Starlette app
    """
    settings = get_settings()

    # Register tools before creating app
    register_tools()

    routes = [
        Route("/sse", sse_handler, methods=["GET"]),
        Route("/messages", messages_handler, methods=["POST"]),
        Route("/health", health_handler, methods=["GET"]),
    ]

    app = Starlette(debug=False, routes=routes)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("MCP server initialized")
    return app


# Create app instance
app = create_app()
