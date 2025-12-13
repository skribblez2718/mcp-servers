#!/bin/bash
# setup-system.sh - System-level setup for recipez-mcp service
# Must be run as root

set -euo pipefail

# Configuration
SERVICE_USER="recipez-mcp"
SERVICE_FILE_SRC="/home/user/projects/mcp-servers/recipez-mcp/recipez-mcp.service"
SERVICE_FILE_DST="/etc/systemd/system/recipez-mcp.service"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    log_error "This script must be run as root"
    exit 1
fi

# Check if service user exists
log_info "Checking if user '${SERVICE_USER}' exists..."
if id "${SERVICE_USER}" &>/dev/null; then
    log_info "User '${SERVICE_USER}' already exists"
else
    log_info "Creating system user '${SERVICE_USER}'..."
    useradd -r -m -s /usr/sbin/nologin "${SERVICE_USER}"
    log_info "User '${SERVICE_USER}' created successfully"
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
log_info "  1. Copy project files to /home/${SERVICE_USER}/recipez-mcp/"
log_info "  2. Run setup-user.sh as the ${SERVICE_USER} user:"
log_info "     sudo -u ${SERVICE_USER} /path/to/setup-user.sh"
log_info "  3. Configure /etc/recipez-mcp/secrets.env with your credentials"
log_info "  4. Enable and start the service:"
log_info "     systemctl enable recipez-mcp"
log_info "     systemctl start recipez-mcp"
