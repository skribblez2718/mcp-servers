#!/usr/bin/env bash
#
# Health check for Open WebUI MCP Server
# Checks if service is running and responding

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SERVICE_NAME="open-webui-mcp.service"
INSTALL_DIR="/opt/open-webui-mcp"

echo "=== Open WebUI MCP Server Health Check ==="
echo ""

# Check 1: Systemd service status
echo -n "1. Service Status: "
if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
    echo -e "${GREEN}RUNNING${NC}"
    SERVICE_RUNNING=1
else
    echo -e "${RED}STOPPED${NC}"
    SERVICE_RUNNING=0
fi

# Check 2: Process existence
echo -n "2. Process Check: "
if pgrep -f "open-webui-mcp" > /dev/null 2>&1; then
    echo -e "${GREEN}FOUND${NC}"
else
    echo -e "${RED}NOT FOUND${NC}"
fi

# Check 3: Configuration file
echo -n "3. Configuration: "
if [[ -f "$INSTALL_DIR/.env" ]] || [[ -f .env ]]; then
    echo -e "${GREEN}EXISTS${NC}"
else
    echo -e "${RED}MISSING${NC}"
fi

# Check 4: Virtual environment
echo -n "4. Virtual Env: "
if [[ -d "$INSTALL_DIR/.venv" ]] || [[ -d .venv ]]; then
    echo -e "${GREEN}EXISTS${NC}"
else
    echo -e "${YELLOW}MISSING${NC}"
fi

# Check 5: Source files
echo -n "5. Source Files: "
if [[ -f "$INSTALL_DIR/src/server.py" ]] || [[ -f src/server.py ]]; then
    echo -e "${GREEN}EXISTS${NC}"
else
    echo -e "${RED}MISSING${NC}"
fi

# Check 6: Open WebUI connectivity (if service running)
if [[ $SERVICE_RUNNING -eq 1 ]]; then
    echo -n "6. Open WebUI API: "

    # Try to read OPENWEBUI_BASE_URL from .env
    if [[ -f "$INSTALL_DIR/.env" ]]; then
        ENV_FILE="$INSTALL_DIR/.env"
    elif [[ -f .env ]]; then
        ENV_FILE=".env"
    else
        echo -e "${YELLOW}SKIPPED (no .env)${NC}"
        exit 0
    fi

    OPENWEBUI_URL=$(grep "^OPENWEBUI_BASE_URL=" "$ENV_FILE" | cut -d'=' -f2)

    if [[ -n "$OPENWEBUI_URL" ]]; then
        if curl -s -f -m 5 "$OPENWEBUI_URL/api/health" > /dev/null 2>&1; then
            echo -e "${GREEN}REACHABLE${NC}"
        else
            echo -e "${YELLOW}UNREACHABLE${NC} ($OPENWEBUI_URL)"
        fi
    else
        echo -e "${YELLOW}SKIPPED (no URL)${NC}"
    fi
fi

echo ""

# Overall status
if [[ $SERVICE_RUNNING -eq 1 ]]; then
    echo -e "Overall Status: ${GREEN}HEALTHY${NC}"
    exit 0
else
    echo -e "Overall Status: ${RED}UNHEALTHY${NC}"
    echo ""
    echo "To start the service:"
    echo "  sudo systemctl start $SERVICE_NAME"
    exit 1
fi
