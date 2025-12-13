#!/usr/bin/env bash
#
# Stop Open WebUI MCP Server (systemd service)

set -euo pipefail

SERVICE_NAME="open-webui-mcp.service"

if ! systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Service $SERVICE_NAME is not running"
    exit 0
fi

echo "Stopping $SERVICE_NAME..."
sudo systemctl stop "$SERVICE_NAME"

echo "Service stopped"
