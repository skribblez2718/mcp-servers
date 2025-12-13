#!/usr/bin/env bash
#
# Restart Open WebUI MCP Server (systemd service)

set -euo pipefail

SERVICE_NAME="open-webui-mcp.service"

echo "Restarting $SERVICE_NAME..."
sudo systemctl restart "$SERVICE_NAME"

echo "Service restarted"
echo ""
echo "Check status with: sudo systemctl status $SERVICE_NAME"
echo "View logs with: sudo journalctl -u $SERVICE_NAME -f"
