#!/usr/bin/env bash
#
# Development setup script for Open WebUI MCP Server
# Sets up local development environment with uv

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

check_uv() {
    if ! command -v uv &> /dev/null; then
        log_error "uv not found. Please install uv first:"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo "  OR"
        echo "  pip install uv"
        exit 1
    fi
    log_info "uv found at $(command -v uv)"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "python3 not found. Please install Python 3.10 or higher"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log_info "Python version: $PYTHON_VERSION"

    # Check Python version >= 3.10
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 10 ]]; then
        log_error "Python 3.10 or higher required, found $PYTHON_VERSION"
        exit 1
    fi
}

create_venv() {
    log_info "Creating virtual environment..."

    if [[ -d .venv ]]; then
        log_warn "Virtual environment already exists at .venv"
        read -p "Recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Removing existing venv..."
            rm -rf .venv
        else
            log_info "Using existing venv"
            return
        fi
    fi

    uv venv
    log_info "Virtual environment created at .venv"
}

install_dependencies() {
    log_info "Installing dependencies with uv..."

    # Install main dependencies
    uv sync

    # Install dev dependencies
    log_info "Installing development dependencies..."
    uv sync --extra dev

    # Install test dependencies
    log_info "Installing test dependencies..."
    uv sync --extra test

    log_info "All dependencies installed"
}

setup_environment() {
    log_info "Setting up environment configuration..."

    if [[ -f .env ]]; then
        log_warn ".env file already exists"
    else
        if [[ -f .env.example ]]; then
            cp .env.example .env
            log_info ".env file created from .env.example"
            log_warn "Please edit .env and set your Open WebUI URL"
        else
            log_error ".env.example not found"
            exit 1
        fi
    fi
}

run_tests() {
    log_info "Running tests to verify setup..."

    if uv run pytest -m unit --tb=short; then
        log_info "Unit tests passed!"
    else
        log_error "Tests failed. Please check the output above"
        exit 1
    fi
}

run_linters() {
    log_info "Running code quality checks..."

    # Black formatting check
    log_info "Checking code formatting (black)..."
    if uv run black --check src tests 2>/dev/null; then
        log_info "Code formatting: PASS"
    else
        log_warn "Code formatting: FAIL (run 'uv run black src tests' to fix)"
    fi

    # Ruff linting
    log_info "Running linter (ruff)..."
    if uv run ruff check src tests 2>/dev/null; then
        log_info "Linting: PASS"
    else
        log_warn "Linting: FAIL (run 'uv run ruff check --fix src tests' to auto-fix)"
    fi

    # Mypy type checking
    log_info "Running type checker (mypy)..."
    if uv run mypy src 2>/dev/null; then
        log_info "Type checking: PASS"
    else
        log_warn "Type checking: FAIL (check mypy output above)"
    fi
}

print_next_steps() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Development Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo ""
    echo "1. Configure your environment:"
    echo -e "   ${GREEN}nano .env${NC}"
    echo "   - Set OPENWEBUI_BASE_URL to your Open WebUI instance"
    echo ""
    echo "2. Activate virtual environment:"
    echo -e "   ${GREEN}source .venv/bin/activate${NC}"
    echo "   (or let uv manage it for you)"
    echo ""
    echo "3. Run the development server:"
    echo -e "   ${GREEN}uv run python src/server.py${NC}"
    echo "   or"
    echo -e "   ${GREEN}./deployment/scripts/start.sh${NC}"
    echo ""
    echo "4. Run tests:"
    echo -e "   ${GREEN}uv run pytest${NC}                    # All tests"
    echo -e "   ${GREEN}uv run pytest -m unit${NC}           # Unit tests only"
    echo -e "   ${GREEN}uv run pytest -m integration${NC}    # Integration tests"
    echo -e "   ${GREEN}uv run pytest --cov=src${NC}         # With coverage"
    echo ""
    echo "5. Code quality:"
    echo -e "   ${GREEN}uv run black src tests${NC}          # Format code"
    echo -e "   ${GREEN}uv run ruff check src tests${NC}     # Lint code"
    echo -e "   ${GREEN}uv run mypy src${NC}                 # Type check"
    echo ""
    echo "6. Configure MCP client (Claude Desktop):"
    echo "   Edit your Claude Desktop config.json:"
    echo "   {"
    echo "     \"mcpServers\": {"
    echo "       \"open-webui\": {"
    echo "         \"command\": \"uv\","
    echo "         \"args\": ["
    echo "           \"--directory\","
    echo "           \"$(pwd)\","
    echo "           \"run\","
    echo "           \"python\","
    echo "           \"src/server.py\""
    echo "         ]"
    echo "       }"
    echo "     }"
    echo "   }"
    echo ""
}

main() {
    log_info "Starting development environment setup..."

    # Get to project root
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    cd "$PROJECT_ROOT"

    log_info "Project root: $PROJECT_ROOT"

    # Setup steps
    check_uv
    check_python
    create_venv
    install_dependencies
    setup_environment
    run_tests

    # Optional: code quality checks
    if [[ "${SKIP_LINTERS:-0}" != "1" ]]; then
        run_linters
    fi

    print_next_steps
}

main "$@"
