#!/bin/bash
# setup-system.sh - Install systemd service file for recipez-mcp
# Must be run as root
#
# This script ONLY handles the systemd service file installation.
# Run setup-user.sh to create the service user and set up the application.

set -euo pipefail

# Configuration
SERVICE_FILE_SRC="/home/user/projects/mcp-servers/recipez-mcp/recipez-mcp.service"
SERVICE_FILE_DST="/etc/systemd/system/recipez-mcp.service"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    log_error "This script must be run as root"
    exit 1
fi

# Verify source service file exists
if [[ ! -f "${SERVICE_FILE_SRC}" ]]; then
    log_error "Service file not found: ${SERVICE_FILE_SRC}"
    exit 1
fi

# Copy service file to systemd directory
log_info "Copying service file to ${SERVICE_FILE_DST}..."
cp "${SERVICE_FILE_SRC}" "${SERVICE_FILE_DST}"

# Set ownership to root
log_info "Setting ownership to root:root..."
chown root:root "${SERVICE_FILE_DST}"

# Set permissions (644 - readable by all, writable by owner)
log_info "Setting permissions to 644..."
chmod 644 "${SERVICE_FILE_DST}"

# Reload systemd
log_info "Reloading systemd daemon..."
systemctl daemon-reload

log_info "System setup complete!"
log_info ""
log_info "Next steps:"
log_info "  1. Run setup-user.sh (as root) to create user and set up application"
log_info "  2. Configure credentials in .env file"
log_info "  3. Enable and start the service:"
log_info "     systemctl enable recipez-mcp"
log_info "     systemctl start recipez-mcp"
