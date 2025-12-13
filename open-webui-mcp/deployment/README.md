# Open WebUI MCP Server - Deployment Guide

This directory contains deployment artifacts for production and development environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Production Deployment](#production-deployment)
- [Development Setup](#development-setup)
- [Service Management](#service-management)
- [Configuration](#configuration)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- **Python 3.10+**: Modern Python with type hints support
- **uv**: Fast Python package manager ([installation guide](https://github.com/astral-sh/uv))
- **systemd**: For production service management (Linux only)

### Optional

- **Open WebUI**: Running instance for API access
- **curl**: For health checks and testing

### Installing uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: pip
pip install uv
```

## Production Deployment

### Quick Start

1. **Run installation script** (requires root):

```bash
sudo ./deployment/scripts/install.sh
```

This script will:
- Install uv if not present
- Create `open-webui-mcp` system user
- Create directories: `/home/open-webui-mcp`, `/var/log/open-webui-mcp`
- Copy source code to `/home/open-webui-mcp`
- Create virtual environment with `uv venv`
- Install dependencies with `uv sync`
- Install systemd service
- Set proper permissions and security hardening

2. **Configure environment**:

```bash
sudo nano /home/open-webui-mcp/.env
```

Set at minimum:
```bash
OPENWEBUI_BASE_URL=http://your-openwebui-instance:8080
# Required: API key from Open WebUI → Settings → Account → API Keys
OPENWEBUI_API_KEY=sk-your_api_key_here
```

3. **Start service**:

```bash
sudo systemctl start open-webui-mcp.service
```

4. **Verify status**:

```bash
sudo systemctl status open-webui-mcp.service
./deployment/scripts/health-check.sh
```

### Manual Installation

If you prefer manual installation:

1. Create user and directories:

```bash
sudo useradd --system --no-create-home --shell /bin/false open-webui-mcp
sudo mkdir -p /home/open-webui-mcp /var/log/open-webui-mcp
```

2. Copy source code:

```bash
sudo cp -r src pyproject.toml .env.example /home/open-webui-mcp/
sudo chown -R open-webui-mcp:open-webui-mcp /home/open-webui-mcp
```

3. Create virtual environment:

```bash
cd /home/open-webui-mcp
sudo -u open-webui-mcp uv venv
sudo -u open-webui-mcp uv sync
```

4. Configure environment:

```bash
sudo cp .env.example .env
sudo nano .env
# IMPORTANT: Set OPENWEBUI_API_KEY from Open WebUI → Settings → Account → API Keys
sudo chmod 600 .env
sudo chown open-webui-mcp:open-webui-mcp .env
```

5. Install systemd service:

```bash
sudo cp deployment/systemd/open-webui-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable open-webui-mcp.service
sudo systemctl start open-webui-mcp.service
```

## Development Setup

### Quick Start

1. **Run setup script**:

```bash
./deployment/scripts/setup.sh
```

This script will:
- Check for uv and Python 3.10+
- Create virtual environment (`.venv`)
- Install dependencies with `uv sync --extra dev --extra test`
- Create `.env` from `.env.example`
- Run tests to verify setup
- Run code quality checks (black, ruff, mypy)

2. **Configure environment**:

```bash
nano .env
```

3. **Start development server**:

```bash
./deployment/scripts/start.sh
# OR
uv run python src/server.py
```

### Manual Development Setup

```bash
# Create virtual environment
uv venv

# Install dependencies
uv sync --extra dev --extra test

# Create environment config
cp .env.example .env
nano .env

# Run tests
uv run pytest

# Start server
uv run python src/server.py
```

## Service Management

### Production (systemd)

```bash
# Start service
sudo systemctl start open-webui-mcp.service

# Stop service
sudo systemctl stop open-webui-mcp.service
# OR
./deployment/scripts/stop.sh

# Restart service
sudo systemctl restart open-webui-mcp.service
# OR
./deployment/scripts/restart.sh

# Check status
sudo systemctl status open-webui-mcp.service
# OR
./deployment/scripts/status.sh

# View logs
sudo journalctl -u open-webui-mcp.service -f
# OR
./deployment/scripts/logs.sh [lines]

# Health check
./deployment/scripts/health-check.sh

# Enable auto-start on boot
sudo systemctl enable open-webui-mcp.service

# Disable auto-start
sudo systemctl disable open-webui-mcp.service
```

### Development

```bash
# Start server (foreground)
./deployment/scripts/start.sh

# OR with uv directly
uv run python src/server.py

# Stop: Ctrl+C
```

## Configuration

### Environment Variables

All configuration is via environment variables (`.env` file):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENWEBUI_BASE_URL` | **Yes** | - | Base URL of Open WebUI instance (e.g., `http://localhost:8080`) |
| `OPENWEBUI_API_KEY` | **Yes** | - | Bearer token for API authentication. Get from: Open WebUI → Settings → Account → API Keys |
| `OPENWEBUI_TIMEOUT` | No | `30` | HTTP request timeout (seconds) |
| `OPENWEBUI_MAX_RETRIES` | No | `3` | Maximum retry attempts for failed requests |
| `OPENWEBUI_RATE_LIMIT` | No | `10` | Client-side rate limit (requests/second) |
| `LOG_LEVEL` | No | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT` | No | `json` | Log format: `json` or `text` |

### Example `.env` File

```bash
# Required: Open WebUI instance URL
OPENWEBUI_BASE_URL=http://localhost:8080

# Required: API key for authentication
# Get from: Open WebUI → Settings → Account → API Keys
OPENWEBUI_API_KEY=sk-your_api_key_here

# Performance tuning
OPENWEBUI_TIMEOUT=30
OPENWEBUI_MAX_RETRIES=3
OPENWEBUI_RATE_LIMIT=10

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### MCP Client Configuration

#### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "open-webui": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/open-webui-mcp",
        "run",
        "python",
        "src/server.py"
      ],
      "env": {
        "OPENWEBUI_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

#### Production (systemd service path)

```json
{
  "mcpServers": {
    "open-webui": {
      "command": "/home/open-webui-mcp/.venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/home/open-webui-mcp",
      "env": {
        "OPENWEBUI_BASE_URL": "http://localhost:8080"
      }
    }
  }
}
```

## Security

### Security Hardening Applied

The systemd service includes comprehensive security hardening:

#### Filesystem Protection
- `ProtectSystem=strict`: Read-only root filesystem
- `ProtectHome=true`: No access to user home directories
- `PrivateTmp=true`: Private `/tmp` directory
- `ReadOnlyPaths=/opt/open-webui-mcp/src`: Immutable source code
- `ReadWritePaths=/var/log/open-webui-mcp`: Logs only writable location

**User Convention**: Service name matches user name (`open-webui-mcp` service runs as `open-webui-mcp` user)

#### Process Restrictions
- `NoNewPrivileges=true`: Cannot gain new privileges
- `PrivateUsers=true`: User namespace isolation
- `LockPersonality=true`: Prevent personality() syscall
- `RestrictRealtime=true`: No realtime scheduling
- `RestrictNamespaces=true`: No namespace creation
- `RestrictSUIDSGID=true`: No SUID/SGID files

#### System Call Filtering
- `SystemCallFilter=@system-service`: Only safe syscalls allowed
- `SystemCallFilter=~@privileged @resources @obsolete`: Block dangerous syscalls

#### Resource Limits
- `CPUQuota=80%`: Maximum 80% CPU usage
- `MemoryMax=1G`: Maximum 1GB memory
- `MemoryHigh=800M`: Soft limit 800MB
- `TasksMax=64`: Maximum 64 tasks/threads
- `LimitNOFILE=4096`: Maximum 4096 open files

#### Network Restrictions
- `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`: Only inet/unix sockets
- Service runs as non-root user (`mcp-user`)

#### Capability Restrictions
- `CapabilityBoundingSet=`: No capabilities
- `AmbientCapabilities=`: No ambient capabilities

### Secret Management

- **No hardcoded secrets**: All secrets in `.env`
- **`.env` never committed**: Listed in `.gitignore`
- **`.env.example` with placeholders only**: Safe to commit
- **File permissions**: `.env` is `600` (owner read/write only)
- **Service user ownership**: `.env` owned by `mcp-user`

### Input Validation

- **Pydantic validation**: All external inputs validated
- **ID format checking**: Alphanumeric + `_-` only
- **Pagination bounds**: `limit` 1-1000, `offset` ≥0
- **Path sanitization**: No `..` traversal, no absolute paths
- **URL encoding**: Safe parameter encoding

### Rate Limiting

- **Token bucket algorithm**: Configurable via `OPENWEBUI_RATE_LIMIT`
- **Default 10 req/s**: Prevents API abuse
- **Per-client basis**: Independent rate limits per MCP client

## Troubleshooting

### Service Won't Start

1. Check service status:
```bash
sudo systemctl status open-webui-mcp.service
```

2. View detailed logs:
```bash
sudo journalctl -u open-webui-mcp.service -n 50
```

3. Check configuration:
```bash
sudo cat /home/open-webui-mcp/.env
```

4. Verify permissions:
```bash
ls -la /home/open-webui-mcp
ls -la /var/log/open-webui-mcp
```

5. Test manually:
```bash
sudo -u open-webui-mcp /home/open-webui-mcp/.venv/bin/python -m src.server
```

### Connection Refused / API Unreachable

1. Verify Open WebUI is running:
```bash
curl http://localhost:8080/api/health
```

2. Check `OPENWEBUI_BASE_URL` and `OPENWEBUI_API_KEY` in `.env`:
```bash
grep OPENWEBUI_BASE_URL /home/open-webui-mcp/.env
grep OPENWEBUI_API_KEY /home/open-webui-mcp/.env
```

3. Test network connectivity:
```bash
ping -c 3 localhost
telnet localhost 8080
```

4. Verify API key validity:
```bash
curl -H "Authorization: Bearer $(grep OPENWEBUI_API_KEY /home/open-webui-mcp/.env | cut -d= -f2)" http://localhost:8080/api/v1/chats
# Should return JSON, not 401 Unauthorized
```

### Rate Limiting Errors

1. Check rate limit setting:
```bash
grep OPENWEBUI_RATE_LIMIT /home/open-webui-mcp/.env
```

2. Increase rate limit if needed:
```bash
sudo nano /home/open-webui-mcp/.env
# Set OPENWEBUI_RATE_LIMIT=20
sudo systemctl restart open-webui-mcp.service
```

### Memory/CPU Limits Exceeded

1. Check resource usage:
```bash
systemctl show open-webui-mcp.service | grep Memory
systemctl show open-webui-mcp.service | grep CPU
```

2. Adjust limits in service file:
```bash
sudo nano /etc/systemd/system/open-webui-mcp.service
# Increase MemoryMax, CPUQuota as needed
sudo systemctl daemon-reload
sudo systemctl restart open-webui-mcp.service
```

### Permission Denied Errors

1. Check file ownership:
```bash
ls -la /home/open-webui-mcp
```

2. Fix ownership if needed:
```bash
sudo chown -R open-webui-mcp:open-webui-mcp /home/open-webui-mcp
sudo chown -R open-webui-mcp:open-webui-mcp /var/log/open-webui-mcp
```

3. Check `.env` permissions:
```bash
ls -l /home/open-webui-mcp/.env
sudo chmod 600 /home/open-webui-mcp/.env
```

### Virtual Environment Issues

1. Recreate virtual environment:
```bash
cd /home/open-webui-mcp
sudo -u open-webui-mcp rm -rf .venv
sudo -u open-webui-mcp uv venv
sudo -u open-webui-mcp uv sync
```

2. Verify uv installation:
```bash
which uv
uv --version
```

### Tests Failing

1. Run tests with verbose output:
```bash
uv run pytest -vv
```

2. Run unit tests only (skip integration):
```bash
uv run pytest -m unit
```

3. Check test dependencies:
```bash
uv sync --extra test
```

4. Generate coverage report:
```bash
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### MCP Client Connection Issues

1. Verify server starts manually:
```bash
uv run python src/server.py
```

2. Check MCP client configuration path:
```bash
# Claude Desktop macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

3. Check MCP client logs:
```bash
# Claude Desktop logs location varies by OS
# Look for connection errors, command not found, etc.
```

4. Test with absolute paths:
```json
{
  "command": "/full/path/to/uv",
  "args": ["--directory", "/full/path/to/open-webui-mcp", "run", "python", "src/server.py"]
}
```

## Directory Structure

```
deployment/
├── README.md                          # This file
├── systemd/
│   └── open-webui-mcp.service        # Systemd service unit file
└── scripts/
    ├── install.sh                     # Production installation
    ├── setup.sh                       # Development setup
    ├── start.sh                       # Start development server
    ├── stop.sh                        # Stop systemd service
    ├── restart.sh                     # Restart systemd service
    ├── status.sh                      # Check service status
    ├── logs.sh                        # View service logs
    └── health-check.sh                # Health check script
```

## Support

For issues, questions, or contributions:
- Check troubleshooting section above
- Review logs: `sudo journalctl -u open-webui-mcp.service -f`
- Run health check: `./deployment/scripts/health-check.sh`
- Check configuration: `.env` file settings
- Verify Open WebUI API: `curl http://localhost:8080/api/health`
