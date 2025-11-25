#!/usr/bin/env bash
#
# View Open WebUI MCP Server logs (systemd service)

set -euo pipefail

SERVICE_NAME="open-webui-mcp.service"

# Follow logs with optional line count argument
LINES="${1:-50}"

echo "Showing last $LINES lines (following)..."
echo "Press Ctrl+C to stop"
echo ""

sudo journalctl -u "$SERVICE_NAME" -n "$LINES" -f
