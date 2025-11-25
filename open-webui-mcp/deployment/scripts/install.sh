#!/usr/bin/env bash
#
# Production installation script for Open WebUI MCP Server
# Installs to /home/open-webui-mcp with systemd service
# Requires: root privileges, uv package manager

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVICE_USER="open-webui-mcp"
INSTALL_DIR="/home/$SERVICE_USER"
LOG_DIR="/var/log/open-webui-mcp"
SERVICE_FILE="open-webui-mcp.service"
SYSTEMD_DIR="/etc/systemd/system"

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

check_uv() {
    # First check if user already exists (created earlier in flow)
    if id "$SERVICE_USER" &>/dev/null; then
        # Check if service user has uv installed
        if sudo -i -u "$SERVICE_USER" command -v uv &> /dev/null; then
            UV_PATH=$(sudo -i -u "$SERVICE_USER" command -v uv)
            log_info "uv found at $UV_PATH"
            return 0
        fi
    fi

    # uv not found, need to install for service user
    log_warn "uv not found for service user. Installing uv..."

    # Ensure service user exists before installing
    if ! id "$SERVICE_USER" &>/dev/null; then
        log_error "Service user $SERVICE_USER must be created before installing uv"
        exit 1
    fi

    # Install uv as the service user (to ~/.local/bin)
    sudo -i -u "$SERVICE_USER" bash <<'EOF'
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH in .profile (for login shells)
if ! grep -q '.local/bin' ~/.profile 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
fi
EOF

    # Verify installation
    if sudo -i -u "$SERVICE_USER" command -v uv &> /dev/null; then
        UV_PATH=$(sudo -i -u "$SERVICE_USER" command -v uv)
        log_info "uv installed successfully at $UV_PATH"
    else
        log_error "Failed to install uv for service user. Please install manually: https://github.com/astral-sh/uv"
        exit 1
    fi
}

create_user() {
    if id "$SERVICE_USER" &>/dev/null; then
        log_info "User $SERVICE_USER already exists"
    else
        log_info "Creating system user $SERVICE_USER with home directory..."
        # Use /bin/bash shell to allow uv installation and environment setup
        useradd --system --create-home --home-dir "$INSTALL_DIR" --shell /bin/bash "$SERVICE_USER"
        # Lock the password for security (prevent login via password)
        passwd -l "$SERVICE_USER" &>/dev/null
        log_info "User $SERVICE_USER created with home at $INSTALL_DIR"
    fi
}

create_directories() {
    log_info "Creating directory structure..."

    # Installation directory created by useradd --create-home
    # Just ensure subdirectories exist
    sudo -u "$SERVICE_USER" mkdir -p "$INSTALL_DIR/src"
    sudo -u "$SERVICE_USER" mkdir -p "$INSTALL_DIR/deployment"

    # Create log directory (needs root)
    mkdir -p "$LOG_DIR"
    chown "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"
    chmod 755 "$LOG_DIR"

    log_info "Directories created"
}

copy_source() {
    log_info "Copying source code to $INSTALL_DIR..."

    # Get script directory (deployment/scripts/)
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

    # Copy files as root (current user may own source files)
    # Then change ownership to service user
    cp -r "$PROJECT_ROOT/src/"* "$INSTALL_DIR/src/"
    cp "$PROJECT_ROOT/pyproject.toml" "$INSTALL_DIR/"
    cp "$PROJECT_ROOT/.env.example" "$INSTALL_DIR/"
    cp "$PROJECT_ROOT/README.md" "$INSTALL_DIR/"
    cp -r "$PROJECT_ROOT/deployment" "$INSTALL_DIR/"

    # Change ownership of all copied files to service user
    chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

    log_info "Source code copied and ownership set"
}

create_venv() {
    log_info "Creating virtual environment with uv..."

    # Run as service user with login shell (loads .profile with PATH)
    sudo -i -u "$SERVICE_USER" bash <<EOF
cd "$INSTALL_DIR"

# Create venv
uv venv

# Install the package and its production dependencies
# Use 'uv pip install' instead of 'uv sync' since we don't have a lock file
uv pip install .
EOF

    log_info "Virtual environment created and dependencies installed"
}

setup_environment() {
    log_info "Setting up environment configuration..."

    if [[ -f "$INSTALL_DIR/.env" ]]; then
        log_warn ".env file already exists, skipping creation"
        log_warn "Please review $INSTALL_DIR/.env manually"
    else
        sudo -u "$SERVICE_USER" cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"
        sudo -u "$SERVICE_USER" chmod 600 "$INSTALL_DIR/.env"
        log_info ".env file created from .env.example"
        log_warn "IMPORTANT: Edit $INSTALL_DIR/.env with your Open WebUI base URL and API key"
    fi
}

set_permissions() {
    log_info "Setting file permissions..."

    # Ownership already correct (files created as service user)
    # Just verify key directories
    chown "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
    chown "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"

    # Set directory permissions
    chmod 755 "$INSTALL_DIR"
    chmod 755 "$LOG_DIR"

    # .env should be readable only by service user (already set in setup_environment)
    if [[ -f "$INSTALL_DIR/.env" ]]; then
        chmod 600 "$INSTALL_DIR/.env"
    fi

    # Scripts should be executable
    chmod 755 "$INSTALL_DIR/deployment/scripts/"*.sh

    log_info "Permissions set"
}

install_systemd_service() {
    log_info "Installing systemd service..."

    # Copy service file
    cp "$INSTALL_DIR/deployment/systemd/$SERVICE_FILE" "$SYSTEMD_DIR/"

    # Set service file permissions
    chmod 644 "$SYSTEMD_DIR/$SERVICE_FILE"

    # Reload systemd daemon
    systemctl daemon-reload

    log_info "Systemd service installed"
}

enable_service() {
    log_info "Enabling systemd service..."

    systemctl enable "$SERVICE_FILE"

    log_info "Service enabled (will start on boot)"
}

run_tests() {
    log_info "Running tests to verify installation..."

    # Run tests as service user with login shell (loads .profile with PATH)
    if sudo -i -u "$SERVICE_USER" bash -c "cd $INSTALL_DIR && uv run pytest -m unit --tb=short" 2>/dev/null; then
        log_info "Tests passed successfully"
    else
        log_warn "Tests failed or test dependencies not installed"
        log_warn "This is not critical for production deployment"
    fi
}

print_post_install() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Installation Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo ""
    echo "1. Configure the service:"
    echo -e "   ${GREEN}sudo nano $INSTALL_DIR/.env${NC}"
    echo "   - Set OPENWEBUI_BASE_URL to your Open WebUI instance"
    echo "   - Set OPENWEBUI_API_KEY to your API key (REQUIRED)"
    echo "     Get API key from: Open WebUI → Settings → Account → API Keys"
    echo ""
    echo "2. Start the service:"
    echo -e "   ${GREEN}sudo systemctl start $SERVICE_FILE${NC}"
    echo ""
    echo "3. Check service status:"
    echo -e "   ${GREEN}sudo systemctl status $SERVICE_FILE${NC}"
    echo ""
    echo "4. View logs:"
    echo -e "   ${GREEN}sudo journalctl -u $SERVICE_FILE -f${NC}"
    echo ""
    echo "5. Configure MCP client (e.g., Claude Desktop):"
    echo "   Add to your MCP client configuration:"
    echo "   {"
    echo "     \"open-webui\": {"
    echo "       \"command\": \"$INSTALL_DIR/.venv/bin/python\","
    echo "       \"args\": [\"$INSTALL_DIR/src/server.py\"],"
    echo "       \"env\": {"
    echo "         \"OPENWEBUI_BASE_URL\": \"http://localhost:8080\""
    echo "       }"
    echo "     }"
    echo "   }"
    echo ""
    echo -e "${YELLOW}Management Scripts:${NC}"
    echo -e "   Start:   ${GREEN}sudo systemctl start $SERVICE_FILE${NC}"
    echo -e "   Stop:    ${GREEN}sudo systemctl stop $SERVICE_FILE${NC}"
    echo -e "   Restart: ${GREEN}sudo systemctl restart $SERVICE_FILE${NC}"
    echo -e "   Status:  ${GREEN}sudo systemctl status $SERVICE_FILE${NC}"
    echo -e "   Logs:    ${GREEN}sudo journalctl -u $SERVICE_FILE -f${NC}"
    echo ""
}

main() {
    log_info "Starting Open WebUI MCP Server installation..."

    # Pre-flight checks
    check_root

    # Installation steps
    create_user
    check_uv  # Check/install uv AFTER creating service user
    create_directories
    copy_source
    create_venv
    setup_environment
    set_permissions
    install_systemd_service
    enable_service

    # Optional: run tests
    if [[ "${SKIP_TESTS:-0}" != "1" ]]; then
        run_tests
    fi

    # Post-installation instructions
    print_post_install
}

main "$@"
