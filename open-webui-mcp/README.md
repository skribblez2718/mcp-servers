# Open WebUI MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready Model Context Protocol (MCP) server providing programmatic access to Open WebUI's REST API. Built with modern Python 3.10+, factory-based architecture, and comprehensive security hardening.

## Table of Contents

- [Features](#features)
- [Project Status](#project-status)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [MCP Client Setup](#mcp-client-setup)
  - [Starting the Server](#starting-the-server)
  - [Claude Code (CLI)](#claude-code-cli)
  - [Claude Desktop](#claude-desktop)
  - [Cursor IDE](#cursor-ide)
  - [Windsurf](#windsurf)
  - [Generic MCP Clients](#generic-mcp-clients)
- [Available Tools](#available-tools)
- [Configuration Reference](#configuration-reference)
- [Architecture](#architecture)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **HTTP SSE Transport**: Production-ready HTTP server with Server-Sent Events for MCP communication
- **329 MCP Tools**: Complete coverage of Open WebUI's REST API (100% of endpoints)
- **Extensible Foundation**: Factory pattern with auto-discovery for easy tool addition
- **Multi-Client Support**: Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client
- **Type-Safe**: 100% type hints with Python 3.10+ syntax and Pydantic validation
- **Security Hardened**: Input validation, rate limiting, error sanitization, path traversal protection
- **Rate Limiting**: Token bucket algorithm prevents API overwhelm (configurable req/sec)
- **Production Ready**: Uvicorn HTTP server, systemd service, comprehensive deployment scripts
- **1296 Test Cases**: Auto-generated test suite with comprehensive coverage
- **Modern Python**: uv-based dependency management, no setup.py, clean project structure

## Project Status

**Current Implementation**: Complete - Full API Coverage

- **✅ Infrastructure**: Complete (exceptions, config, 4 core utilities)
- **✅ Data Models**: 17 Pydantic models (chat, model, user, errors)
- **✅ Services**: OpenWebUIClient with GET/POST/PUT/PATCH/DELETE + file upload + streaming
- **✅ Tool Foundation**: BaseTool protocol, ToolFactory with lazy loading and file-based discovery
- **✅ 329 MCP Tools**: Complete coverage of all Open WebUI REST API endpoints
- **✅ Test Suite**: 1296 auto-generated test cases
- **✅ Deployment**: Systemd service, installation scripts, operational tooling
- **✅ Code Generation**: Jinja2-based tool generator from OpenAPI spec

**API Coverage by Category**:
- Chats: 37 tools
- Models: 8 tools
- Users: 22 tools
- Knowledge: 12 tools
- Files: 12 tools
- Functions: 17 tools
- Tools: 17 tools
- Channels: 14 tools
- Admin/Config: 30 tools
- Ollama/OpenAI: 50 tools
- And 130+ more across 33 resource categories

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP Client Layer                        │
│  (Claude Code, Claude Desktop, Cursor, Windsurf, etc.)      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP SSE transport
┌──────────────────────▼──────────────────────────────────────┐
│                    MCP Server (server.py)                    │
│  Handlers: list_tools, call_tool                            │
│  Protocol: MCP 1.0 with HTTP SSE transport                  │
│  Endpoints: /sse (GET), /messages (POST)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Tool Factory (factory.py)                   │
│  Lazy Loading │ Dependency Injection │ Auto-Discovery       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Tools Layer (tools/)                      │
│  chat_list │ chat_get │ model_list │ user_list │ health    │
│  Each tool: validate input → call service → return result   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               Services Layer (services/client.py)            │
│  OpenWebUIClient: HTTP client with rate limiting            │
│  Rate Limiter: Token bucket (10 req/s default)              │
│  Error Handling: HTTP status → domain exceptions            │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│                  Open WebUI REST API                         │
│  GET /api/v1/chats, /api/v1/models, /api/health, etc.      │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Patterns**:
- **Factory Pattern**: Auto-discovers tools via filesystem scan, lazy loading for fast startup
- **Dependency Injection**: Tools receive configured client, no global state
- **Protocol-Based**: BaseTool protocol enables structural subtyping
- **Error Transformation**: HTTP errors → domain exceptions → sanitized MCP responses

## Prerequisites

### Required

- **Python 3.10+**: Modern Python with type hints and pattern matching
- **uv**: Fast Python package manager ([install guide](https://github.com/astral-sh/uv))
- **MCP Client**: Claude Desktop, Cursor, Windsurf, or compatible client

### Optional

- **Open WebUI**: Running instance (local or remote) for API access
- **systemd**: For production deployment (Linux only)

### Installing uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: pip
pip install uv

# Verify installation
uv --version
```

## Quick Start

### 1. Clone and Install

```bash
# Clone repository
cd /path/to/mcp-servers/open-webui-mcp

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment

Edit `.env`:

```bash
# Required: Your Open WebUI instance URL
OPENWEBUI_BASE_URL=http://localhost:8080

# Required: Bearer token for API authentication
# Get from: Open WebUI → Settings → Account → API Keys
# Format: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENWEBUI_API_KEY=sk-your_api_key_here

# Optional: Performance tuning (defaults shown)
OPENWEBUI_TIMEOUT=30
OPENWEBUI_MAX_RETRIES=3
OPENWEBUI_RATE_LIMIT=10

# Optional: Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 3. Test Installation

```bash
# Run tests
uv run pytest

# Start HTTP SSE server (default: http://127.0.0.1:8000)
uv run python -m src.server

# Custom host/port via environment variables
PORT=8080 HOST=0.0.0.0 uv run python -m src.server
# Press Ctrl+C to stop
```

### 4. Configure Your MCP Client

See [MCP Client Setup](#mcp-client-setup) below for detailed client-specific instructions.

## MCP Client Setup

> **Note**: This server uses **HTTP SSE transport** (not stdio). You must first start the server, then configure your MCP client to connect to it.

### Starting the Server

Before configuring any client, start the MCP server:

```bash
# Navigate to project directory
cd /path/to/open-webui-mcp

# Start the server (default: http://127.0.0.1:8000)
uv run python -m src.server

# Or with custom host/port
PORT=8080 HOST=0.0.0.0 uv run python -m src.server
```

The server exposes two endpoints:
- `GET /sse` - SSE connection endpoint for MCP protocol
- `POST /messages` - Message handling endpoint

### Claude Code (CLI)

**Quick Add Command** (recommended):

```bash
claude mcp add open-webui --transport sse http://127.0.0.1:8000/sse
```

This adds the MCP server to your Claude Code configuration. Use `--scope` flag to control where it's added:

```bash
# Add to project-specific config (.mcp.json in current directory)
claude mcp add open-webui --transport sse http://127.0.0.1:8000/sse --scope project

# Add to user-wide config (~/.claude/settings.json)
claude mcp add open-webui --transport sse http://127.0.0.1:8000/sse --scope user
```

**Manual Configuration** (alternative):

Add to `.mcp.json` in your project root or `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "open-webui": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

### Claude Desktop

**Configuration File Location**:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**HTTP SSE Configuration**:

```json
{
  "mcpServers": {
    "open-webui": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Important Notes**:
1. **Start server first**: The MCP server must be running before Claude Desktop connects
2. **Match the port**: Ensure the URL matches the port your server is running on
3. **Restart Claude Desktop**: After editing config, fully quit and restart Claude

**Troubleshooting Claude Desktop**:
- **Tools not appearing**: Check Claude Desktop logs at `~/Library/Logs/Claude/mcp*.log` (macOS)
- **Connection refused**: Ensure the MCP server is running (`uv run python -m src.server`)
- **Invalid JSON**: Validate config with `python -m json.tool < claude_desktop_config.json`

### Cursor IDE

**Configuration File Location**:
- **macOS**: `~/Library/Application Support/Cursor/mcp_settings.json`
- **Windows**: `%APPDATA%\Cursor\mcp_settings.json`
- **Linux**: `~/.config/Cursor/mcp_settings.json`

**HTTP SSE Configuration**:

```json
{
  "mcpServers": {
    "open-webui": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Cursor-Specific Notes**:
1. **Start server first**: Run `uv run python -m src.server` before using Cursor
2. **IDE Integration**: Cursor may require restart after config change (Cmd+Q on macOS, close all windows)
3. **Workspace Settings**: Cursor supports workspace-specific MCP config in `.cursor/mcp_settings.json`
4. **Tool Invocation**: Use `@open-webui` prefix in Cursor chat to invoke MCP tools

**Troubleshooting Cursor**:
- **Tools not loading**: Open Cursor Developer Tools (Help → Toggle Developer Tools) and check Console
- **Connection refused**: Ensure the MCP server is running
- **Workspace config priority**: Workspace `.cursor/mcp_settings.json` overrides global config

### Windsurf

**Configuration File Location**:
- **macOS**: `~/Library/Application Support/Windsurf/mcp_config.json`
- **Windows**: `%APPDATA%\Windsurf\mcp_config.json`
- **Linux**: `~/.config/Windsurf/mcp_config.json`

**HTTP SSE Configuration**:

```json
{
  "mcpServers": {
    "open-webui": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Windsurf-Specific Notes**:
1. **Start server first**: Run `uv run python -m src.server` before using Windsurf
2. **Beta Software**: Windsurf MCP support may evolve, check their documentation for updates
3. **Environment Isolation**: Each Windsurf project can have separate MCP config
4. **Reload Command**: Use Command Palette (Cmd+Shift+P) → "Reload MCP Servers" after config changes

**Troubleshooting Windsurf**:
- **Check MCP status**: Command Palette → "MCP: Show Status" to see registered servers
- **Connection refused**: Ensure the MCP server is running
- **Logs location**: View logs via Command Palette → "MCP: Show Logs"

### Generic MCP Clients

For other MCP-compatible clients (custom tools, IDE plugins, etc.):

**HTTP SSE Configuration Parameters**:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `type` | `sse` | Transport type (HTTP Server-Sent Events) |
| `url` | `http://127.0.0.1:8000/sse` | SSE endpoint URL |

**Generic JSON Configuration**:

```json
{
  "mcpServers": {
    "open-webui": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

**Server Configuration** (via environment variables in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `8000` | Server port |
| `OPENWEBUI_BASE_URL` | (required) | Open WebUI instance URL |
| `OPENWEBUI_API_KEY` | (required) | API key for authentication |

**Verification**:

After starting the server and configuring your client:

1. **Check Server Running**: `curl http://127.0.0.1:8000/sse` should connect (SSE stream)
2. **List Tools**: Use MCP client's tool list command (e.g., in Claude: "What tools are available?")
3. **Test Tool**: Try a simple tool like `admin_health`: "Check Open WebUI health status"
4. **Check Logs**: Server logs to stdout (JSON format by default)

## Available Tools

### Tier 1 Tools (Implemented)

#### Chat Management

**`chat_list`** - List all chats with pagination

```typescript
// Input Schema
{
  limit?: number;      // Items per page (1-1000, default: 10)
  offset?: number;     // Pagination offset (≥0, default: 0)
  archived?: boolean;  // Show only archived chats (default: false)
}

// Output
{
  chats: Array<Chat>;       // Array of chat objects
  total: number;            // Total chats available
  limit: number;            // Items per page
  offset: number;           // Current offset
  has_next: boolean;        // More pages available
}
```

**Example Usage**: "List the last 20 chats" → `{"limit": 20, "offset": 0}`

---

**`chat_get`** - Get specific chat by ID

```typescript
// Input Schema
{
  chat_id: string;     // Chat identifier (alphanumeric + _-)
}

// Output
{
  chat: Chat;          // Full chat object with messages
}
```

**Example Usage**: "Show me chat abc123" → `{"chat_id": "abc123"}`

---

#### Model Management

**`model_list`** - List available models

```typescript
// Input Schema
{
  limit?: number;      // Items per page (1-1000, default: 20)
  offset?: number;     // Pagination offset (≥0, default: 0)
}

// Output
{
  models: Array<Model>;     // Array of model objects
  total: number;            // Total models available
  limit: number;
  offset: number;
  has_next: boolean;
}
```

**Example Usage**: "What models are available?" → `{"limit": 20}`

---

#### User Management

**`user_list`** - List users (requires admin privileges)

```typescript
// Input Schema
{
  limit?: number;      // Items per page (1-1000, default: 20)
  offset?: number;     // Pagination offset (≥0, default: 0)
}

// Output
{
  users: Array<User>;       // Array of user objects
  total: number;
  limit: number;
  offset: number;
  has_next: boolean;
}
```

**Example Usage**: "Show all users" → `{"limit": 100}`

**Note**: Requires admin-level API key (OPENWEBUI_API_KEY) for authentication

---

#### Admin Operations

**`admin_health`** - Check Open WebUI instance health

```typescript
// Input Schema
{}  // No parameters required

// Output
{
  status: string;           // "healthy" | "unhealthy"
  version?: string;         // Open WebUI version
  database?: string;        // Database status
  uptime?: number;          // Uptime in seconds
}
```

**Example Usage**: "Is Open WebUI healthy?" → `{}`

---

### Extensibility

**132 Additional Tools Ready for Implementation**

The server architecture maps 138 Open WebUI API endpoints. Currently 6 are implemented as Tier 1 tools. Remaining tools follow the same pattern:

**Tier 2 (Knowledge, Files, Retrieval)** - 30 tools:
- Knowledge bases: `knowledge_list`, `knowledge_get`, `knowledge_create`, etc.
- File management: `file_list`, `file_get`, `file_upload`, etc.
- Retrieval: `retrieval_query`, `retrieval_vector_search`, etc.

**Tier 3 (Functions)** - 12 tools:
- Function management: `function_list`, `function_create`, `function_call`, etc.

**Tier 4 (Miscellaneous)** - 90 tools:
- Prompts, tags, folders, evaluations, tasks, channels, memories, etc.

**Adding New Tools**: See [Development → Adding Tools](#adding-tools) section below.

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENWEBUI_BASE_URL` | **Yes** | - | Base URL of Open WebUI instance (e.g., `http://localhost:8080`) |
| `OPENWEBUI_API_KEY` | **Yes** | - | Bearer token for API authentication. Get from: Open WebUI → Settings → Account → API Keys (format: `sk-xxxxx...`) |
| `HOST` | No | `127.0.0.1` | HTTP server bind address (use `0.0.0.0` to expose externally) |
| `PORT` | No | `8000` | HTTP server port (1-65535) |
| `OPENWEBUI_TIMEOUT` | No | `30` | HTTP request timeout in seconds (1-300) |
| `OPENWEBUI_MAX_RETRIES` | No | `3` | Maximum retry attempts for failed requests (0-10) |
| `OPENWEBUI_RATE_LIMIT` | No | `10` | Rate limit in requests per second (1-1000) |
| `LOG_LEVEL` | No | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `LOG_FORMAT` | No | `json` | Log format (`json` or `text`) |

### Configuration Validation

The server validates configuration on startup:

- `OPENWEBUI_BASE_URL`: Must start with `http://` or `https://`, trailing slash stripped
- `OPENWEBUI_TIMEOUT`: Must be ≥1 second
- `OPENWEBUI_MAX_RETRIES`: Must be ≥0
- `OPENWEBUI_RATE_LIMIT`: Must be ≥1 request/second
- `LOG_LEVEL`: Must be valid Python logging level

**Invalid Configuration Example**:

```bash
OPENWEBUI_BASE_URL=localhost:8080  # ❌ Missing http://
OPENWEBUI_TIMEOUT=0                # ❌ Must be ≥1
OPENWEBUI_RATE_LIMIT=0             # ❌ Must be ≥1
```

**Validation Errors**: Server exits with clear error message if configuration is invalid.

### Rate Limiting

**Token Bucket Algorithm**:
- **Capacity**: `OPENWEBUI_RATE_LIMIT` requests per second
- **Refill Rate**: 1 token per (1/rate) seconds
- **Burst Handling**: Up to `rate` concurrent requests allowed
- **Blocking**: Requests block (await) until token available, no 429 errors internally

**Example**:
- `OPENWEBUI_RATE_LIMIT=10`: Allows 10 requests/second sustained, burst of 10 simultaneous requests
- `OPENWEBUI_RATE_LIMIT=5`: Allows 5 requests/second, 200ms minimum between requests

**Tuning**:
- **Low traffic**: 5-10 req/s sufficient
- **High traffic**: 50-100 req/s (check Open WebUI server capacity)
- **Defensive**: 1 req/s ensures no overwhelm (slow but safe)

## Architecture

### Directory Structure

```
open-webui-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py                 # MCP server entry point
│   ├── config.py                 # Configuration (Pydantic Settings)
│   ├── exceptions.py             # Custom exception hierarchy
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging_utils.py      # Structured JSON logging
│   │   ├── validation.py         # Input validation (ToolInputValidator)
│   │   ├── rate_limiter.py       # Token bucket rate limiter
│   │   ├── error_handler.py      # Error sanitization
│   │   └── url_builder.py        # Safe URL construction
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py               # BaseModel, PaginatedResponse[T]
│   │   ├── chat.py               # Chat, Message, MessageContent
│   │   ├── model.py              # Model, ModelConfig
│   │   ├── user.py               # User, UserProfile, Role
│   │   └── errors.py             # ErrorResponse, ErrorDetail
│   ├── services/
│   │   ├── __init__.py
│   │   └── client.py             # OpenWebUIClient (HTTP client)
│   └── tools/
│       ├── __init__.py
│       ├── base.py               # BaseTool protocol
│       ├── factory.py            # ToolFactory (lazy loading, DI)
│       ├── chats/
│       │   ├── __init__.py
│       │   ├── chat_list_tool.py
│       │   └── chat_get_tool.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── model_list_tool.py
│       ├── users/
│       │   ├── __init__.py
│       │   └── user_list_tool.py
│       └── admin/
│           ├── __init__.py
│           └── admin_health_tool.py
├── tests/
│   ├── conftest.py               # Shared fixtures
│   ├── fixtures/
│   │   └── openapi_responses.py  # Realistic mocks
│   ├── unit/                     # Unit tests (9 files)
│   └── integration/              # Integration tests (1 file)
├── deployment/
│   ├── README.md                 # Deployment guide
│   ├── systemd/
│   │   └── open-webui-mcp.service
│   └── scripts/
│       ├── install.sh            # Production install
│       ├── setup.sh              # Development setup
│       ├── start.sh              # Start dev server
│       ├── stop.sh               # Stop service
│       ├── restart.sh            # Restart service
│       ├── status.sh             # Check status
│       ├── logs.sh               # View logs
│       └── health-check.sh       # Health verification
├── .env.example                  # Environment template
├── pyproject.toml                # Project metadata (uv-compatible)
├── pytest.ini                    # Test configuration
└── README.md                     # This file
```

### Component Responsibilities

**Layer 1: Infrastructure**
- `config.py`: Pydantic Settings for environment validation
- `exceptions.py`: Custom exception hierarchy (6 exceptions)
- `utils/`: Stateless utilities (logging, validation, rate limiting, error handling)

**Layer 2: Data Models**
- `models/base.py`: Generic base models with type parameters
- `models/{resource}.py`: Domain models (Chat, Model, User, etc.)
- All models use Pydantic for validation

**Layer 3: Services**
- `services/client.py`: OpenWebUIClient (async HTTP client with httpx)
- Handles: HTTP requests, rate limiting, error transformation, response parsing

**Layer 4: Tool Foundation**
- `tools/base.py`: BaseTool protocol (structural subtyping)
- `tools/factory.py`: ToolFactory (auto-discovery, lazy loading, DI)

**Layer 5: Tools**
- `tools/{resource}/{tool}_tool.py`: Individual tool implementations
- Each tool: Extends BaseTool, implements `get_definition()` and `execute()`

**Layer 6: MCP Server**
- `server.py`: MCP protocol handlers (`list_tools`, `call_tool`)
- Stdio transport, asyncio event loop

### Factory Pattern

**Auto-Discovery**:

```python
# Tool discovery flow
1. Factory scans src/tools/*/ directories
2. Finds all *_tool.py files (e.g., chat_list_tool.py)
3. Extracts tool name from filename (chat_list)
4. Infers module path: src.tools.chats.chat_list_tool
5. Caches tool class: ChatListTool
```

**Lazy Loading**:

```python
# Tool creation flow (on first use)
1. MCP client calls tool: call_tool("chat_list", args)
2. Factory checks cache: chat_list not loaded
3. Factory imports module: import src.tools.chats.chat_list_tool
4. Factory instantiates tool: ChatListTool(client=..., config=...)
5. Factory caches instance
6. Tool executes: tool.execute(args)
7. Subsequent calls use cached instance
```

**Benefits**:
- **Fast Startup**: <100ms (loads tools on demand, not at startup)
- **No Registration**: Adding tool = create file, no factory changes needed
- **Memory Efficient**: Only used tools loaded into memory

### Error Flow

**Error Transformation Pipeline**:

```
HTTP Response (httpx)
  │
  ├─ 400 Bad Request ──→ ValidationError
  ├─ 401 Unauthorized ─→ AuthError
  ├─ 403 Forbidden ────→ AuthError
  ├─ 404 Not Found ────→ NotFoundError
  ├─ 429 Too Many ─────→ RateLimitError (with retry_after)
  ├─ 500 Server Error ─→ ServerError
  ├─ 503 Unavailable ──→ ServerError
  └─ Other ────────────→ HTTPError
  │
  ▼
Domain Exception
  │
  ▼
Error Handler (sanitize_error)
  │ - Logs full exception with stack trace
  │ - Removes sensitive paths/keys
  │ - Returns generic message
  ▼
MCP Error Response (to client)
```

**Sanitization**:
- Logs have full details (stack trace, request params, response body)
- MCP responses have generic messages ("Service temporarily unavailable")
- No internal paths, config values, or implementation details exposed

## Development

### Setup Development Environment

```bash
# Clone repository
cd /path/to/mcp-servers/open-webui-mcp

# Install dev dependencies
uv sync --extra dev --extra test

# Create .env
cp .env.example .env

# Run tests
uv run pytest

# Run linters
uv run black src/
uv run ruff src/
uv run mypy src/
```

### Code Quality Standards

**Type Hints**: 100% coverage required
```python
# ✅ Good
def validate_id(value: str, max_length: int = 255) -> str: ...

# ❌ Bad
def validate_id(value, max_length=255): ...
```

**Docstrings**: Google-style for all public interfaces
```python
def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute tool operation.

    Args:
        arguments: Tool input parameters

    Returns:
        Tool result as dict

    Raises:
        ValidationError: If arguments invalid
        HTTPError: If API call fails
    """
```

**File Size**: Maximum 200 lines per file
- Encourages SRP (Single Responsibility Principle)
- Makes code navigable and reviewable
- Largest current file: `client.py` (209 LOC - acceptable, monolithic client)

**Modern Python**: Use Python 3.10+ features
```python
# ✅ Use union operator
def get_value() -> str | None: ...

# ❌ Don't use Optional (deprecated style)
from typing import Optional
def get_value() -> Optional[str]: ...
```

### Testing

**Run Tests**:

```bash
# All tests
uv run pytest

# Unit tests only (fast, <5s)
uv run pytest -m unit

# Integration tests (requires Open WebUI)
uv run pytest -m integration

# With coverage
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Test Structure**:

```
tests/
├── conftest.py              # Shared fixtures (10 fixtures)
├── fixtures/
│   └── openapi_responses.py # Realistic API mocks
├── unit/                    # Unit tests (153 test cases)
│   ├── test_config.py
│   ├── test_exceptions.py
│   ├── utils/
│   ├── services/
│   └── tools/
└── integration/             # Integration tests (8 test cases)
    └── test_local_api.py
```

**Coverage Target**: >80% overall, 100% critical paths
- Critical paths: validation, error sanitization, rate limiting, exceptions
- Lower coverage OK: Pydantic models (self-validating), MCP boilerplate

### Adding Tools

**Step 1: Create Tool File**

```bash
# Create file in appropriate directory
touch src/tools/{resource}/{tool_name}_tool.py
```

**Step 2: Implement BaseTool**

```python
"""Tool description."""

from typing import Any
from ..base import BaseTool
from ...utils.validation import ToolInputValidator

class MyToolNameTool(BaseTool):
    """Brief description.

    Longer description if needed.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition."""
        return {
            "name": "my_tool_name",
            "description": "What this tool does",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute tool operation."""
        self._log_execution_start(arguments)

        # 1. Validate input
        param1 = arguments.get("param1")
        ToolInputValidator.validate_id(param1)  # Example validation

        # 2. Call API
        response = await self.client.get(
            f"/api/v1/resource/{param1}"
        )

        # 3. Transform response
        result = {
            "data": response.get("data"),
            "status": "success"
        }

        self._log_execution_end(result)
        return result
```

**Step 3: No Registration Needed!**

Factory auto-discovers via filename pattern `*_tool.py`.

**Step 4: Test Tool**

```python
# tests/unit/tools/test_my_tool_name_tool.py
import pytest
from src.tools.{resource}.my_tool_name_tool import MyToolNameTool

@pytest.mark.asyncio
async def test_my_tool_definition():
    """Test tool definition."""
    tool = MyToolNameTool(client=mock_client, config=mock_config)
    definition = tool.get_definition()
    assert definition["name"] == "my_tool_name"
    assert "inputSchema" in definition

@pytest.mark.asyncio
async def test_my_tool_execute(mock_client):
    """Test tool execution."""
    mock_client.get.return_value = {"data": "test"}
    tool = MyToolNameTool(client=mock_client, config=mock_config)
    result = await tool.execute({"param1": "test123"})
    assert result["status"] == "success"
```

**Step 5: Verify**

```bash
# Run tests
uv run pytest tests/unit/tools/test_my_tool_name_tool.py

# Start server and check tool appears
uv run python -m src.server
# In MCP client: "What tools are available?"
# Should see "my_tool_name" in list
```

**Tool Template**: See `src/tools/chats/chat_list_tool.py` for complete reference implementation.

## Deployment

### Production Deployment

See [deployment/README.md](deployment/README.md) for comprehensive deployment guide.

**Quick Start (Linux with systemd)**:

```bash
# Run installation script (requires root)
sudo ./deployment/scripts/install.sh

# Configure
sudo nano /opt/open-webui-mcp/.env

# Start service
sudo systemctl start open-webui-mcp.service

# Verify
./deployment/scripts/health-check.sh
```

**Features**:
- Systemd service with 22 security hardening directives
- Runs as low-privilege `mcp-user` (no login, no home directory)
- Resource limits (1GB memory, 80% CPU, 64 tasks)
- Auto-restart on failure
- Read-only source code at runtime
- Comprehensive health checks

### Development Deployment

```bash
# Run setup script (no root required)
./deployment/scripts/setup.sh

# Start development server (foreground)
./deployment/scripts/start.sh

# Or with uv directly
uv run python -m src.server
```

## Troubleshooting

### Common Issues

#### 1. Server Won't Start

**Symptoms**: `uv run python -m src.server` fails

**Causes & Solutions**:

```bash
# Check 1: uv installed?
uv --version
# If not: curl -LsSf https://astral.sh/uv/install.sh | sh

# Check 2: Dependencies installed?
ls .venv/
# If not: uv sync

# Check 3: .env file exists?
ls .env
# If not: cp .env.example .env

# Check 4: OPENWEBUI_BASE_URL set?
grep OPENWEBUI_BASE_URL .env
# If not: echo "OPENWEBUI_BASE_URL=http://localhost:8080" >> .env

# Check 5: Python version?
python --version  # Should be 3.10+
# If not: Install Python 3.10+
```

#### 2. MCP Client Can't Connect

**Symptoms**: Tools not appearing in Claude Desktop/Cursor

**Causes & Solutions**:

```bash
# Check 1: MCP config path correct?
# Claude Desktop: ~/Library/Application Support/Claude/claude_desktop_config.json
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Check 2: Absolute paths used?
# ❌ Bad: "cwd": "~/projects/open-webui-mcp"
# ✅ Good: "cwd": "/Users/username/projects/open-webui-mcp"

# Check 3: Restart MCP client after config change
# Fully quit and restart (not just reload window)

# Check 4: Check MCP client logs
# Claude Desktop: ~/Library/Logs/Claude/mcp*.log
tail -f ~/Library/Logs/Claude/mcp-*.log

# Check 5: Test server manually
uv run python -m src.server
# Should start without errors, press Ctrl+C to stop
```

#### 3. Connection Refused to Open WebUI

**Symptoms**: Tool execution fails with "Connection refused"

**Causes & Solutions**:

```bash
# Check 1: Open WebUI running?
curl http://localhost:8080/api/health
# If connection refused: Start Open WebUI

# Check 2: Correct URL?
grep OPENWEBUI_BASE_URL .env
# Should be: http://localhost:8080 (or your server URL)

# Check 3: Network accessible?
ping localhost
# If fails: Check firewall/network config

# Check 4: HTTPS vs HTTP?
# ❌ Bad: OPENWEBUI_BASE_URL=https://localhost:8080 (if Open WebUI uses HTTP)
# ✅ Good: OPENWEBUI_BASE_URL=http://localhost:8080
```

#### 4. Rate Limiting Errors

**Symptoms**: Requests slow or time out

**Causes & Solutions**:

```bash
# Check current rate limit
grep OPENWEBUI_RATE_LIMIT .env
# Default: 10 requests/second

# Increase limit if needed
echo "OPENWEBUI_RATE_LIMIT=50" >> .env

# Or decrease if overwhelming Open WebUI
echo "OPENWEBUI_RATE_LIMIT=5" >> .env

# Restart server after change
```

#### 5. Permission Denied (Production)

**Symptoms**: Systemd service fails with permission errors

**Causes & Solutions**:

```bash
# Check 1: Files owned by open-webui-mcp user?
ls -la /home/open-webui-mcp/
# Should show: open-webui-mcp:open-webui-mcp

# Check 2: .env readable?
ls -la /home/open-webui-mcp/.env
# Should show: -rw------- (600 permissions)

# Check 3: Log directory writable?
ls -la /var/log/open-webui-mcp/
# Should show: open-webui-mcp:open-webui-mcp

# Fix permissions:
sudo chown -R open-webui-mcp:open-webui-mcp /home/open-webui-mcp
sudo chmod 600 /home/open-webui-mcp/.env
sudo chown -R open-webui-mcp:open-webui-mcp /var/log/open-webui-mcp
```

#### 6. Tests Failing

**Symptoms**: `uv run pytest` fails

**Causes & Solutions**:

```bash
# Check 1: Test dependencies installed?
uv sync --extra test

# Check 2: Run specific test for details
uv run pytest tests/unit/test_config.py -v

# Check 3: Integration tests require Open WebUI
uv run pytest -m unit  # Skip integration tests

# Check 4: Coverage failure?
uv run pytest --cov=src --cov-report=term-missing
# Add tests for uncovered lines
```

#### 7. Memory/CPU Limits Hit (Production)

**Symptoms**: Service killed or throttled

**Causes & Solutions**:

```bash
# Check resource usage
systemctl show open-webui-mcp.service | grep Memory
systemctl show open-webui-mcp.service | grep CPU

# Increase limits in systemd service
sudo nano /etc/systemd/system/open-webui-mcp.service
# Change: MemoryMax=1G → MemoryMax=2G
# Change: CPUQuota=80% → CPUQuota=150%

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart open-webui-mcp.service
```

#### 8. Invalid JSON Config

**Symptoms**: MCP client fails to parse config

**Causes & Solutions**:

```bash
# Validate JSON syntax
python -m json.tool < ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Common errors:
# - Missing comma between objects
# - Trailing comma before closing brace
# - Unescaped quotes in strings
# - Comments (JSON doesn't support // or /* */)

# Fix and validate again
```

#### 9. Tool Returns Empty Results

**Symptoms**: Tool executes but returns no data

**Causes & Solutions**:

```bash
# Check 1: Open WebUI has data?
curl http://localhost:8080/api/v1/chats
# Should return JSON with chats

# Check 2: API key set?
# All requests require OPENWEBUI_API_KEY
grep OPENWEBUI_API_KEY .env
# Should be set (format: sk-xxxxx...)

# Check 3: API key valid?
# Test with curl
curl -H "Authorization: Bearer sk-your_api_key" http://localhost:8080/api/v1/chats
# Should return JSON without 401 error

# Check 4: Pagination?
# Use limit=100 to get more results
# "List the last 100 chats"

# Check 5: Check logs
journalctl -u open-webui-mcp.service -f
# Look for API errors, 401 Unauthorized
```

#### 10. 401 Unauthorized Errors

**Symptoms**: Tool execution fails with "401 Unauthorized" or "Unauthorized"

**Causes & Solutions**:

```bash
# Check 1: OPENWEBUI_API_KEY set?
grep OPENWEBUI_API_KEY .env
# If empty: Set your API key (from Open WebUI → Settings → Account → API Keys)

# Check 2: API key format correct?
# Should be: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (format: sk- prefix, 32+ hex chars)
echo $OPENWEBUI_API_KEY | head -c 3
# Should print: sk-

# Check 3: API key valid in Open WebUI?
# - Go to Open WebUI → Settings → Account → API Keys
# - Verify key is active (not revoked)
# - Try regenerating if invalid

# Check 4: Header correctly formed?
# The server automatically adds: Authorization: Bearer {api_key}
# Verify with curl:
curl -H "Authorization: Bearer $OPENWEBUI_API_KEY" http://localhost:8080/api/v1/chats
# Should return JSON, not 401

# Check 5: Restart server after changing OPENWEBUI_API_KEY
./deployment/scripts/restart.sh
```

**Difference between API Key and JWT Token**:
- **API Key**: Long-lived token from Settings → Account → API Keys (format: `sk-xxxxx`)
- **JWT Token**: Short-lived authentication token from login (different format)
- Both work with `Authorization: Bearer` header format

---

#### 11. uv Command Not Found

**Symptoms**: `uv: command not found`

**Causes & Solutions**:

```bash
# Check 1: uv installed?
which uv

# If not found, install:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Check 2: Shell PATH updated?
echo $PATH | grep cargo
# uv installs to ~/.cargo/bin

# If not in PATH, add to shell config:
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or use absolute path:
~/.cargo/bin/uv --version
```

### Debug Mode

**Enable Debug Logging**:

```bash
# In .env
LOG_LEVEL=DEBUG
LOG_FORMAT=text  # Easier to read than JSON for debugging

# Restart server
./deployment/scripts/restart.sh

# View logs
./deployment/scripts/logs.sh
```

**Debug Output Includes**:
- Request parameters (before validation)
- Validation results
- API calls (URL, params, headers)
- Rate limiter state (tokens available)
- Response data (before transformation)
- Execution timing (per tool call)

### Getting Help

**Resources**:
1. **Documentation**: This README, [deployment/README.md](deployment/README.md), [CONTRIBUTING.md](CONTRIBUTING.md)
2. **API Reference**: [TOOLS.md](TOOLS.md)
3. **FAQ**: [FAQ.md](FAQ.md)
4. **Issues**: GitHub Issues (if repository public)
5. **Logs**: Check server logs (`LOG_LEVEL=DEBUG` for details)

## Future Enhancements

### Planned Features (TODO)

**Authentication** (Priority: High)
- [x] Bearer token authentication (OPENWEBUI_API_KEY implementation) - COMPLETE
- [x] API key validation on startup - COMPLETE
- [ ] Token refresh mechanism
- [ ] Scope-based access control per tool

**Remaining Tools** (Priority: Medium)
- [ ] Tier 2: Knowledge, files, retrieval tools (30 tools)
- [ ] Tier 3: Functions tools (12 tools)
- [ ] Tier 4: Miscellaneous tools (90 tools)
- [ ] Tool generation script (automate boilerplate)

**Streaming Support** (Priority: Medium)
- [ ] StreamingService for SSE parsing
- [ ] `chat_stream_completion` tool for real-time responses
- [ ] WebSocket support for bidirectional streaming
- [ ] Async iterators for streaming responses

**Performance** (Priority: Low)
- [ ] Response caching layer (Redis/in-memory)
- [ ] Connection pooling optimization
- [ ] Batch request support (multiple tools in one call)
- [ ] Lazy data model validation (defer until needed)

**Developer Experience** (Priority: Low)
- [ ] Interactive tool tester CLI
- [ ] Tool template generator (`uv run tool-generator {name}`)
- [ ] Mock Open WebUI server for testing
- [ ] VS Code extension for tool development

**Observability** (Priority: Low)
- [ ] Prometheus metrics export
- [ ] OpenTelemetry tracing
- [ ] Request/response logging to database
- [ ] Performance dashboard

### Contributing

Want to help implement these features? See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup guide
- Code standards and style guide
- Pull request process
- Tool implementation tutorial
- Testing requirements

**High-Impact Contributions**:
1. Implement Tier 2 tools (knowledge, files, retrieval)
2. Add bearer token authentication
3. Create tool generation script
4. Improve test coverage (>90%)
5. Add streaming support

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code of conduct
- Development setup
- Code standards (type hints, docstrings, file size)
- Testing requirements (>80% coverage)
- Pull request process
- Tool addition guide

**Quick Contribution Workflow**:

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-new-tool`
3. Implement tool following [Adding Tools](#adding-tools) guide
4. Add tests: `tests/unit/tools/test_my_tool.py`
5. Run linters: `uv run black src/ && uv run ruff src/ && uv run mypy src/`
6. Run tests: `uv run pytest`
7. Commit: `git commit -m "Add my_new_tool for resource X"`
8. Push: `git push origin feature/my-new-tool`
9. Create pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Open WebUI MCP Server Contributors

---

**Project Status**: Production-ready with complete API coverage. 329 MCP tools covering 100% of Open WebUI's REST API endpoints.

**Version**: 1.0.0 (Full API Coverage)

**Last Updated**: 2025-12-11
