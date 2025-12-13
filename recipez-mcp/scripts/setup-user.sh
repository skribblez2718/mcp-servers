#!/bin/bash
# setup-user.sh - Application setup for recipez-mcp
# Must be run as the recipez-mcp user

set -euo pipefail

# Configuration
EXPECTED_USER="recipez-mcp"
PROJECT_DIR="/home/recipez-mcp/recipez-mcp"

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

# Verify running as correct user
CURRENT_USER=$(whoami)
if [[ "${CURRENT_USER}" != "${EXPECTED_USER}" ]]; then
    log_error "This script must be run as '${EXPECTED_USER}', not '${CURRENT_USER}'"
    log_error "Use: sudo -u ${EXPECTED_USER} $0"
    exit 1
fi

# Verify project directory exists
if [[ ! -d "${PROJECT_DIR}" ]]; then
    log_error "Project directory not found: ${PROJECT_DIR}"
    log_error "Please copy the project files first"
    exit 1
fi

# Install uv package manager
log_info "Installing uv package manager..."
if command -v uv &>/dev/null; then
    log_info "uv is already installed"
else
    curl -LsSf https://astral.sh/uv/install.sh | sh
    log_info "uv installed successfully"
fi

# Add uv to PATH for current session
export PATH="${HOME}/.local/bin:${PATH}"

# Verify uv is available
if ! command -v uv &>/dev/null; then
    log_error "uv installation failed or not in PATH"
    exit 1
fi

log_info "uv version: $(uv --version)"

# Navigate to project directory
log_info "Changing to project directory: ${PROJECT_DIR}"
cd "${PROJECT_DIR}"

# Copy .env.example to .env if .env doesn't exist
if [[ -f ".env" ]]; then
    log_warn ".env already exists, skipping copy"
else
    if [[ -f ".env.example" ]]; then
        log_info "Copying .env.example to .env..."
        cp .env.example .env
        log_info ".env created - remember to edit it with your credentials"
    else
        log_error ".env.example not found in ${PROJECT_DIR}"
        exit 1
    fi
fi

# Create virtual environment
log_info "Creating virtual environment..."
if [[ -d ".venv" ]]; then
    log_warn "Virtual environment already exists"
else
    uv venv
    log_info "Virtual environment created"
fi

# Install dependencies
log_info "Installing dependencies..."
uv sync
log_info "Dependencies installed successfully"

log_info ""
log_info "User setup complete!"
log_info ""
log_info "Next steps:"
log_info "  1. Edit ${PROJECT_DIR}/.env with your credentials:"
log_info "     - RECIPEZ_BASE_URL"
log_info "     - RECIPEZ_JWT_TOKEN"
log_info "  2. Create secrets file for systemd (as root):"
log_info "     sudo mkdir -p /etc/recipez-mcp"
log_info "     sudo cp ${PROJECT_DIR}/.env /etc/recipez-mcp/secrets.env"
log_info "     sudo chown ${EXPECTED_USER}:${EXPECTED_USER} /etc/recipez-mcp/secrets.env"
log_info "     sudo chmod 600 /etc/recipez-mcp/secrets.env"
log_info "  3. Start the service (as root):"
log_info "     sudo systemctl start recipez-mcp"
