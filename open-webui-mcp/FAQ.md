# Open WebUI MCP Server - Frequently Asked Questions

Common questions and answers about setup, configuration, troubleshooting, and usage.

## Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Multi-Client Configuration](#multi-client-configuration)
- [Troubleshooting](#troubleshooting)
- [Performance & Optimization](#performance--optimization)
- [Security](#security)
- [Development & Contributing](#development--contributing)

## General Questions

### What is the Open WebUI MCP Server?

The Open WebUI MCP Server is a Model Context Protocol (MCP) server that provides programmatic access to Open WebUI's REST API. It allows MCP clients (like Claude Desktop, Cursor, Windsurf) to interact with Open WebUI through natural language or structured tool calls.

### What can I do with it?

Currently implemented (6 tools):
- List and retrieve chats
- List available AI models
- List users (admin)
- Check system health

Planned (132 additional tools):
- Knowledge base management
- File operations
- Retrieval and search
- Function management
- Prompts, tags, folders, etc.

### Do I need Open WebUI running?

Yes. The MCP server acts as a bridge between MCP clients and Open WebUI's API. You need:
1. Open WebUI instance running (local or remote)
2. Network access to Open WebUI (http://localhost:8080 or custom URL)
3. Valid API key for authentication (all API requests require authentication)

### Is this an official Open WebUI project?

No, this is a community-developed MCP server for Open WebUI. It's not officially maintained by the Open WebUI team.

### What's the current status?

**Status**: Production-ready foundation with extensible architecture

- **Phase 4-6 Complete**: Source code, tests, deployment artifacts
- **6 of 138 tools implemented**: Core functionality demonstrated
- **Test Coverage**: >80% (161 test cases)
- **Documentation**: Comprehensive (README, CONTRIBUTING, TOOLS, FAQ)

### Is it stable?

Yes, for implemented features:
- 100% type hints with Pydantic validation
- Comprehensive error handling and sanitization
- Rate limiting prevents API overwhelm
- >80% test coverage
- Security hardened (systemd service with 22 directives)

Remaining 132 tools follow the same proven pattern.

## Installation & Setup

### What are the prerequisites?

**Required**:
- Python 3.10 or higher
- uv package manager
- MCP client (Claude Desktop, Cursor, Windsurf, etc.)

**Optional**:
- Open WebUI instance for testing
- systemd (for production deployment on Linux)

### How do I install uv?

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: pip
pip install uv

# Verify
uv --version
```

### What's the quickest way to get started?

```bash
# 1. Clone and install
cd /path/to/open-webui-mcp
uv sync

# 2. Configure
cp .env.example .env
# Edit .env: OPENWEBUI_BASE_URL=http://localhost:8080

# 3. Test
uv run pytest

# 4. Configure MCP client (see Multi-Client Configuration section)
```

### Do I need to install dependencies globally?

No! uv creates a project-local virtual environment (`.venv/`). All dependencies are isolated.

### Can I use pip instead of uv?

Not recommended. The project is designed for uv (pyproject.toml-based, no setup.py). While theoretically possible with pip, uv provides:
- Faster dependency resolution
- Better caching
- Native pyproject.toml support
- Reproducible builds

## Multi-Client Configuration

### Which MCP clients are supported?

**Fully Supported** (with specific configs):
- Claude Desktop (Anthropic's desktop app)
- Cursor IDE
- Windsurf

**Generic Support**:
- Any MCP-compatible client via stdio transport

### How do I configure Claude Desktop?

**Config File Location**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Config Example**:
```json
{
  "mcpServers": {
    "open-webui": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/open-webui-mcp",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "OPENWEBUI_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

**Important**: Use absolute paths, not `~/` or relative paths.

### Why aren't tools appearing in Claude Desktop?

Common causes:
1. **Invalid JSON**: Validate with `python -m json.tool < config.json`
2. **Relative paths**: Use absolute paths (`/Users/name/...` not `~/...`)
3. **Claude not restarted**: Fully quit (Cmd+Q) and restart
4. **uv not in PATH**: Verify with `which uv`
5. **Server errors**: Check logs at `~/Library/Logs/Claude/mcp*.log`

### How do I configure Cursor?

**Config File**: `~/Library/Application Support/Cursor/mcp_settings.json`

**Config Example** (same as Claude Desktop):
```json
{
  "mcpServers": {
    "open-webui": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path", "python", "-m", "src.server"],
      "env": {"OPENWEBUI_BASE_URL": "http://localhost:8080"}
    }
  }
}
```

**Cursor-Specific**:
- Restart Cursor after config change (close all windows)
- Use `@open-webui` prefix to invoke tools
- Check Developer Tools Console for errors

### How do I configure Windsurf?

**Config File**: `~/Library/Application Support/Windsurf/mcp_config.json`

**Config Example**: Same as Claude Desktop/Cursor

**Windsurf-Specific**:
- Command Palette: "Reload MCP Servers" after config change
- Check status: "MCP: Show Status"
- View logs: "MCP: Show Logs"

### Can I use different configs for dev vs. prod?

Yes! Two patterns:

**Development** (uv command):
```json
{
  "command": "uv",
  "args": ["run", "--directory", "/path/to/project", "python", "-m", "src.server"]
}
```

**Production** (venv python):
```json
{
  "command": "/opt/open-webui-mcp/.venv/bin/python",
  "args": ["-m", "src.server"],
  "cwd": "/opt/open-webui-mcp"
}
```

### Where do environment variables go?

**Three Options** (in precedence order):

1. **MCP client config** (highest priority):
   ```json
   "env": {
     "OPENWEBUI_BASE_URL": "http://localhost:8080",
     "OPENWEBUI_RATE_LIMIT": "50"
   }
   ```

2. **`.env` file** in project directory

3. **System environment** (lowest priority)

## API Keys & Authentication

### How do I get an API key?

**Steps**:
1. Open your Open WebUI instance in a browser
2. Go to: **Settings → Account → API Keys**
3. Click **"Create API Key"** or **"Generate Key"**
4. Copy the API key (format: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
5. Add to your `.env` file: `OPENWEBUI_API_KEY=sk-your_api_key_here`

**API Key Format**:
- Starts with `sk-`
- Followed by 32+ hexadecimal characters
- Example: `sk-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### What's the difference between API Key and JWT Token?

**API Key**:
- Long-lived token (doesn't expire unless revoked)
- Get from: Settings → Account → API Keys
- Format: `sk-xxxxx...` (starts with `sk-`)
- Use case: Service-to-service authentication, long-term access

**JWT Token**:
- Short-lived token (expires after period of time)
- Get from: Login/authentication endpoint
- Format: Different from API key (typically starts with `eyJ...`)
- Use case: Web session authentication, temporary access

**Both work the same way** with the MCP server:
- Both sent via `Authorization: Bearer {token}` header
- Both set via `OPENWEBUI_API_KEY` environment variable
- Both authenticate API requests the same way

**Recommendation**: Use API Key for service-to-service access (more reliable, long-lived).

### Why am I getting "401 Unauthorized" errors?

**Causes**:
1. `OPENWEBUI_API_KEY` not set in `.env`
2. API key is invalid or revoked
3. API key is inactive in Open WebUI
4. API key format is wrong (should start with `sk-`)

**Solutions**:
1. **Check if set**: `grep OPENWEBUI_API_KEY .env`
2. **Verify format**: Should start with `sk-`, at least 32 characters
3. **Verify in Open WebUI**: Settings → Account → API Keys (check if active/not revoked)
4. **Regenerate key**: If expired/invalid, delete and create new key in Settings
5. **Restart server**: `./deployment/scripts/restart.sh` (if production)

**Test with curl**:
```bash
# If you see JSON response (not 401): key is valid
curl -H "Authorization: Bearer sk-your_api_key" http://localhost:8080/api/v1/chats

# If you see 401 Unauthorized: key is invalid
curl -v -H "Authorization: Bearer invalid_key" http://localhost:8080/api/v1/chats
```

### Can I use the same API key in multiple places?

Yes! An API key can be used:
- Multiple MCP clients
- Multiple servers
- Multiple machines

**Security Note**: Treat API keys like passwords
- Don't commit to git (use `.env`, which is in `.gitignore`)
- Don't share via email/chat
- Revoke if compromised
- Regenerate periodically for security

## Troubleshooting

### Server won't start

**Symptom**: `uv run python -m src.server` fails

**Checklist**:
1. `uv --version` → uv installed?
2. `ls .venv/` → dependencies installed? (`uv sync` if not)
3. `ls .env` → env file exists? (`cp .env.example .env` if not)
4. `grep OPENWEBUI_BASE_URL .env` → URL configured?
5. `python --version` → Python 3.10+?

### Connection refused to Open WebUI

**Symptom**: Tools fail with "Connection refused"

**Checklist**:
1. `curl http://localhost:8080/api/health` → Open WebUI running?
2. Check `OPENWEBUI_BASE_URL` in `.env` → correct URL?
3. Firewall blocking connection?
4. HTTP vs. HTTPS mismatch?

### Tools return empty results

**Possible Causes**:
1. **No data**: Open WebUI has no chats/models/users
2. **Authentication**: Endpoint requires `OPENWEBUI_API_KEY`
3. **Pagination**: Default limit too small (increase limit)

**Solutions**:
- Create test data in Open WebUI
- Set `OPENWEBUI_API_KEY` if needed
- Use higher limit: "List the last 100 chats"

### Rate limiting too slow

**Symptom**: Requests taking longer than expected

**Solution**: Increase rate limit
```bash
# .env
OPENWEBUI_RATE_LIMIT=50  # Default is 10
```

Restart server after change.

### How do I enable debug logging?

```bash
# .env
LOG_LEVEL=DEBUG
LOG_FORMAT=text  # Easier to read than JSON

# Restart server
./deployment/scripts/restart.sh  # Production
# Or Ctrl+C and restart development server
```

### Where are the logs?

**Development**: stdout (terminal)

**Production** (systemd):
```bash
# View logs
journalctl -u open-webui-mcp.service -f

# Last 50 lines
./deployment/scripts/logs.sh

# Last 100 lines
./deployment/scripts/logs.sh 100
```

## Performance & Optimization

### What's the recommended rate limit?

Depends on usage:

| Scenario | Recommended | Reasoning |
|----------|-------------|-----------|
| Single user, local Open WebUI | 10-20 req/s | Low latency, high capacity |
| Multiple users, local | 5-10 req/s | Shared resources |
| Remote Open WebUI | 5 req/s | Network latency |
| Shared Open WebUI server | 1-5 req/s | Conservative, prevents overwhelm |

**Start conservative (5 req/s), increase if needed.**

### How do I measure performance?

**Enable debug logging**:
```bash
LOG_LEVEL=DEBUG
```

**Look for**:
- Tool execution time: `[DEBUG] tool=chat_list duration_ms=234`
- Rate limiter waits: `[DEBUG] Rate limiter: waiting 0.2s`
- API response time: `[DEBUG] API call: GET /api/v1/chats took 150ms`

### What's the startup time?

**<100ms** thanks to lazy loading:
- Tools loaded on demand, not at startup
- First tool call may be slightly slower (one-time import)
- Subsequent calls use cached instances

### Does it use a lot of memory?

**Typical usage**: 50-100 MB

- Minimal overhead (no heavy dependencies)
- Tools loaded lazily (only used tools in memory)
- No caching layer (stateless server)

### Can I deploy multiple instances?

Yes! Each MCP client connection spawns independent server process:
- No shared state between instances
- Each has own rate limiter
- No coordination needed

**Systemd service** runs single instance, but MCP clients can each have their own server process.

## Security

### Is it secure?

**Yes**, with proper configuration:

**Security Measures**:
- Input validation prevents injection
- Rate limiting prevents abuse
- Error sanitization prevents info leakage
- No hardcoded secrets (environment variables)
- Systemd service runs as low-privilege user
- Resource limits prevent DoS

**Security Hardening** (production):
- 22 systemd security directives
- Read-only source code at runtime
- Private /tmp, isolated namespaces
- System call filtering
- No capabilities

### Do I need authentication?

**Currently**: No (tools work without API key)

**Future**: Bearer token authentication
- Set `OPENWEBUI_API_KEY` environment variable
- Automatic header injection: `Authorization: Bearer {token}`
- Scope-based access control per tool

Admin tools (like `user_list`) will require auth when implemented.

### Should I expose it to the internet?

**No**, not recommended:

**Why**:
- MCP protocol uses stdio (not HTTP)
- Designed for local MCP client ↔ server communication
- No built-in HTTPS/TLS
- No authentication yet

**If needed**:
- Use systemd service with strict firewall rules
- Place behind authenticated proxy
- Enable all security hardening
- Monitor logs closely

### How are secrets managed?

**Best Practices**:
1. **`.env` file**: Store all secrets here
2. **File permissions**: `chmod 600 .env` (owner read/write only)
3. **`.gitignore`**: `.env` excluded from version control
4. **Production**: systemd `EnvironmentFile` with 600 permissions

**Never**:
- Commit `.env` to git
- Include secrets in MCP client config (use `.env` instead)
- Share `.env` file

## Development & Contributing

### How do I add a new tool?

**Quick Steps**:
1. Create `src/tools/{resource}/{tool_name}_tool.py`
2. Extend `BaseTool`, implement `get_definition()` and `execute()`
3. Add tests in `tests/unit/tools/test_{tool_name}_tool.py`
4. Run `uv run pytest` to verify

**Detailed Guide**: See [CONTRIBUTING.md](CONTRIBUTING.md#adding-new-tools)

**Tool Template**: `src/tools/chats/chat_list_tool.py`

### What coding standards do I need to follow?

**Required**:
- 100% type hints (Python 3.10+ syntax)
- Google-style docstrings
- Files ≤200 LOC (SRP)
- Tests for all new code (>80% coverage)
- Pass linters: black, ruff, mypy

**See**: [CONTRIBUTING.md - Code Standards](CONTRIBUTING.md#code-standards)

### How do I run tests?

```bash
# All tests
uv run pytest

# Unit tests only (fast)
uv run pytest -m unit

# Integration tests (requires Open WebUI)
uv run pytest -m integration

# With coverage
uv run pytest --cov=src --cov-report=html
```

### Can I contribute even if I'm new to Python/MCP?

**Absolutely!**

**Beginner-Friendly Contributions**:
- Fix typos in documentation
- Add examples to README
- Improve error messages
- Add tests for existing code
- Implement simple tools (following template)

**Resources**:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Complete guide
- [TOOLS.md](TOOLS.md) - API reference
- Existing tools as examples

### Where do I ask questions?

**Options**:
1. **GitHub Issues**: Bug reports, feature requests
2. **GitHub Discussions**: Questions, ideas, help
3. **Documentation**: README, CONTRIBUTING, TOOLS, FAQ

---

## Still Have Questions?

**Documentation**:
- [README.md](README.md) - Main documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [TOOLS.md](TOOLS.md) - API reference
- [deployment/README.md](deployment/README.md) - Deployment guide

**Support**:
- GitHub Issues (bugs, features)
- GitHub Discussions (questions, help)
- Check server logs (`LOG_LEVEL=DEBUG`)

---

**Last Updated**: 2025-11-24
**Version**: 0.1.0
