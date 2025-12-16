#!/bin/bash
# setup-user.sh - Set up recipez-mcp application environment
# Must be run as root
#
# Prerequisites:
#   User must already exist: useradd --system --shell /bin/false -m recipez-mcp
#
# This script:
# 1. Copies project files to the user's home directory
# 2. Installs uv and sets up the Python environment
# 3. Creates .env from .env.example
# 4. Creates virtual environment and installs dependencies

set -euo pipefail

# Configuration
SERVICE_USER="recipez-mcp"
PROJECT_SRC="/home/user/projects/mcp-servers/recipez-mcp"
PROJECT_DST="/home/${SERVICE_USER}/recipez-mcp"

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

# Verify user exists
if ! id "${SERVICE_USER}" &>/dev/null; then
    log_error "User '${SERVICE_USER}' does not exist"
    log_error "Create it first: useradd --system --shell /bin/false -m ${SERVICE_USER}"
    exit 1
fi

# Verify source project exists
if [[ ! -d "${PROJECT_SRC}" ]]; then
    log_error "Project source not found: ${PROJECT_SRC}"
    exit 1
fi

# Step 1: Copy project files
log_info "Copying project files to ${PROJECT_DST}..."
if [[ -d "${PROJECT_DST}" ]]; then
    log_warn "Project directory already exists, updating files..."
fi
mkdir -p "${PROJECT_DST}"
# Copy all files except .git, .venv, __pycache__, .env (but include .env.example)
rsync -a --delete \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='.mypy_cache' \
    --exclude='.pytest_cache' \
    --exclude='.ruff_cache' \
    "${PROJECT_SRC}/" "${PROJECT_DST}/"

# Step 2: Set ownership
log_info "Setting ownership to ${SERVICE_USER}:${SERVICE_USER}..."
chown -R "${SERVICE_USER}:${SERVICE_USER}" "${PROJECT_DST}"

# Step 3: Install uv for the service user
# Use su -s to override /bin/false shell
log_info "Installing uv for ${SERVICE_USER}..."
if su -s /bin/bash "${SERVICE_USER}" -c 'test -f ~/.local/bin/uv'; then
    log_info "uv is already installed"
else
    su -s /bin/bash "${SERVICE_USER}" -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
    log_info "uv installed successfully"
fi

# Step 4: Copy .env.example to .env if .env doesn't exist
log_info "Setting up environment file..."
if [[ -f "${PROJECT_DST}/.env" ]]; then
    log_warn ".env already exists, skipping copy"
else
    if [[ -f "${PROJECT_DST}/.env.example" ]]; then
        su -s /bin/bash "${SERVICE_USER}" -c "cp ${PROJECT_DST}/.env.example ${PROJECT_DST}/.env"
        log_info ".env created from .env.example"
    else
        log_error ".env.example not found in ${PROJECT_DST}"
        exit 1
    fi
fi

# Step 5: Create virtual environment and install dependencies
log_info "Creating virtual environment and installing dependencies..."
su -s /bin/bash "${SERVICE_USER}" -c "
    export PATH=\"\${HOME}/.local/bin:\${PATH}\"
    cd ${PROJECT_DST}
    uv venv
    uv sync
"
log_info "Virtual environment created and dependencies installed"

log_info ""
log_info "User setup complete!"
log_info ""
log_info "Next steps:"
log_info "  1. Edit ${PROJECT_DST}/.env with your credentials:"
log_info "     - RECIPEZ_BASE_URL"
log_info "     - RECIPEZ_JWT_TOKEN"
log_info "  2. Run setup-system.sh to install the systemd service"
log_info "  3. Enable and start the service:"
log_info "     systemctl enable recipez-mcp"
log_info "     systemctl start recipez-mcp"
