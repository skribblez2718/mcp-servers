#!/usr/bin/env bash
#
# Check Open WebUI MCP Server status (systemd service)

set -euo pipefail

SERVICE_NAME="open-webui-mcp.service"

echo "=== Service Status ==="
sudo systemctl status "$SERVICE_NAME" --no-pager || true

echo ""
echo "=== Recent Logs ==="
sudo journalctl -u "$SERVICE_NAME" -n 20 --no-pager
