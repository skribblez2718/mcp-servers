#!/usr/bin/env bash
#
# Start Open WebUI MCP Server in development mode

set -euo pipefail

# Get to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

# Check if .env exists
if [[ ! -f .env ]]; then
    echo "Error: .env file not found"
    echo "Please run deployment/scripts/setup.sh first"
    exit 1
fi

# Load environment
set -a
source .env
set +a

echo "Starting Open WebUI MCP Server..."
echo "Base URL: $OPENWEBUI_BASE_URL"
echo "Log Level: ${LOG_LEVEL:-INFO}"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run with uv
exec uv run python src/server.py
