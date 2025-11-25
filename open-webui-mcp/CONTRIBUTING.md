# Contributing to Open WebUI MCP Server

Thank you for considering contributing to the Open WebUI MCP Server! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Adding New Tools](#adding-new-tools)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

### Our Standards

- **Be Respectful**: Treat all contributors with respect
- **Be Collaborative**: Work together to solve problems
- **Be Professional**: Maintain professional communication
- **Be Inclusive**: Welcome contributions from all backgrounds

### Unacceptable Behavior

- Harassment, discrimination, or trolling
- Personal attacks or insults
- Publishing others' private information
- Other conduct inappropriate in a professional setting

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- Basic understanding of:
  - Python async/await
  - REST APIs
  - Model Context Protocol (MCP)

### First-Time Contributions

Great first issues for new contributors:

1. **Add a new tool**: Implement one of the remaining 132 tools (see [README.md](README.md#extensibility))
2. **Improve documentation**: Fix typos, add examples, clarify instructions
3. **Add tests**: Increase test coverage for existing code
4. **Fix bugs**: Check open issues for bug reports

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/open-webui-mcp.git
cd open-webui-mcp

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/open-webui-mcp.git
```

### 2. Install Dependencies

```bash
# Install development dependencies
uv sync --extra dev --extra test

# Create .env file
cp .env.example .env

# Edit .env with your Open WebUI URL
# OPENWEBUI_BASE_URL=http://localhost:8080
```

### 3. Verify Setup

```bash
# Run tests
uv run pytest

# Run linters
uv run black --check src/
uv run ruff check src/
uv run mypy src/

# Start server
uv run python -m src.server
# Press Ctrl+C to stop
```

### 4. Create Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/my-new-feature
```

## Project Structure

### Directory Layout

```
open-webui-mcp/
├── src/                        # Source code
│   ├── config.py               # Configuration (Pydantic Settings)
│   ├── exceptions.py           # Custom exceptions
│   ├── server.py               # MCP server entry point
│   ├── utils/                  # Utilities
│   │   ├── logging_utils.py    # Structured logging
│   │   ├── validation.py       # Input validation
│   │   ├── rate_limiter.py     # Rate limiting
│   │   ├── error_handler.py    # Error sanitization
│   │   └── url_builder.py      # URL construction
│   ├── models/                 # Data models (Pydantic)
│   │   ├── base.py             # BaseModel, PaginatedResponse
│   │   ├── chat.py             # Chat models
│   │   ├── model.py            # Model models
│   │   ├── user.py             # User models
│   │   └── errors.py           # Error models
│   ├── services/               # Services layer
│   │   └── client.py           # OpenWebUIClient (HTTP)
│   └── tools/                  # MCP tools
│       ├── base.py             # BaseTool protocol
│       ├── factory.py          # ToolFactory (DI, auto-discovery)
│       ├── chats/              # Chat tools
│       ├── models/             # Model tools
│       ├── users/              # User tools
│       └── admin/              # Admin tools
├── tests/                      # Test suite
│   ├── conftest.py             # Shared fixtures
│   ├── fixtures/               # Test fixtures
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── deployment/                 # Deployment artifacts
│   ├── systemd/                # Systemd service
│   └── scripts/                # Installation scripts
├── .env.example                # Environment template
├── pyproject.toml              # Project metadata
├── pytest.ini                  # Test configuration
├── README.md                   # Main documentation
├── CONTRIBUTING.md             # This file
├── TOOLS.md                    # API reference
└── FAQ.md                      # FAQ
```

### Module Responsibilities

**`src/config.py`**: Configuration management with Pydantic Settings. Validates environment variables on startup.

**`src/exceptions.py`**: Custom exception hierarchy. All exceptions inherit from `HTTPError` base class.

**`src/utils/`**: Stateless utility functions. No side effects, pure functions where possible.

**`src/models/`**: Pydantic data models for API requests/responses. All external data validated through models.

**`src/services/client.py`**: HTTP client for Open WebUI API. Handles rate limiting, error transformation, response parsing.

**`src/tools/`**: MCP tool implementations. Each tool extends `BaseTool` protocol, implements `get_definition()` and `execute()`.

**`src/server.py`**: MCP server entry point. Implements `list_tools` and `call_tool` handlers, manages stdio transport.

## Adding New Tools

### Step 1: Choose a Tool

Check the list of unimplemented tools:

- **Tier 2** (30 tools): Knowledge, files, retrieval (higher priority)
- **Tier 3** (12 tools): Functions
- **Tier 4** (90 tools): Miscellaneous (lower priority)

Example: Let's implement `knowledge_list` tool.

### Step 2: Create Data Models (if needed)

If the tool requires new models:

```python
# src/models/knowledge.py
"""Knowledge base data models."""

from typing import Any
from datetime import datetime
from .base import BaseModel

class Knowledge(BaseModel):
    """Knowledge base entry."""

    id: str
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

class KnowledgeCollection(BaseModel):
    """Collection of knowledge items."""

    id: str
    name: str
    items: list[Knowledge]
```

### Step 3: Create Tool File

```bash
# Create directory if needed
mkdir -p src/tools/knowledge

# Create tool file
touch src/tools/knowledge/knowledge_list_tool.py
```

### Step 4: Implement Tool

```python
# src/tools/knowledge/knowledge_list_tool.py
"""Knowledge list tool - List all knowledge bases."""

from typing import Any
from ..base import BaseTool
from ...models.knowledge import Knowledge
from ...models.base import PaginatedResponse
from ...utils.validation import ToolInputValidator


class KnowledgeListTool(BaseTool):
    """List all knowledge bases with pagination.

    Retrieves knowledge bases accessible to the current user.
    """

    def get_definition(self) -> dict[str, Any]:
        """Get MCP tool definition.

        Returns:
            Tool definition with schema
        """
        return {
            "name": "knowledge_list",
            "description": "List all knowledge bases with pagination support",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of items to return (1-1000)",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset in the list",
                        "default": 0,
                        "minimum": 0
                    }
                },
                "required": []
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute knowledge list retrieval.

        Args:
            arguments: Tool arguments with limit, offset

        Returns:
            Dict with knowledge bases list and pagination info

        Raises:
            ValidationError: If arguments invalid
            HTTPError: If API call fails
        """
        self._log_execution_start(arguments)

        # Validate parameters
        limit = arguments.get("limit", 20)
        offset = arguments.get("offset", 0)
        limit, offset = ToolInputValidator.validate_pagination(limit, offset)

        # Call API
        params = {"limit": limit, "offset": offset}
        response_data = await self.client.get("/api/v1/knowledge", params=params)

        # Transform response
        result = {
            "knowledge": response_data.get("data", []),
            "total": response_data.get("total", 0),
            "limit": limit,
            "offset": offset,
            "has_next": response_data.get("has_next", False)
        }

        self._log_execution_end(result)
        return result
```

### Step 5: Create Tests

```python
# tests/unit/tools/knowledge/test_knowledge_list_tool.py
"""Tests for knowledge_list tool."""

import pytest
from src.tools.knowledge.knowledge_list_tool import KnowledgeListTool


@pytest.mark.asyncio
async def test_knowledge_list_definition(mock_client, mock_config):
    """Test tool definition."""
    tool = KnowledgeListTool(client=mock_client, config=mock_config)
    definition = tool.get_definition()

    assert definition["name"] == "knowledge_list"
    assert "inputSchema" in definition
    assert definition["inputSchema"]["type"] == "object"


@pytest.mark.asyncio
async def test_knowledge_list_execute_defaults(mock_client, mock_config):
    """Test execution with default parameters."""
    mock_client.get.return_value = {
        "data": [{"id": "kb1", "name": "Test KB"}],
        "total": 1
    }

    tool = KnowledgeListTool(client=mock_client, config=mock_config)
    result = await tool.execute({})

    assert "knowledge" in result
    assert result["limit"] == 20
    assert result["offset"] == 0
    mock_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_knowledge_list_execute_custom_params(mock_client, mock_config):
    """Test execution with custom parameters."""
    mock_client.get.return_value = {"data": [], "total": 0}

    tool = KnowledgeListTool(client=mock_client, config=mock_config)
    result = await tool.execute({"limit": 50, "offset": 10})

    assert result["limit"] == 50
    assert result["offset"] == 10


@pytest.mark.asyncio
async def test_knowledge_list_validation_error(mock_client, mock_config):
    """Test validation error for invalid parameters."""
    tool = KnowledgeListTool(client=mock_client, config=mock_config)

    with pytest.raises(ValidationError):
        await tool.execute({"limit": 2000})  # Exceeds maximum
```

### Step 6: Run Tests

```bash
# Run specific test file
uv run pytest tests/unit/tools/knowledge/test_knowledge_list_tool.py -v

# Run all tests
uv run pytest

# Check coverage
uv run pytest --cov=src/tools/knowledge --cov-report=term-missing
```

### Step 7: Verify Tool Registration

```bash
# Start server
uv run python -m src.server

# In MCP client (e.g., Claude Desktop):
# "What tools are available?"
# Should see "knowledge_list" in the list

# Test tool:
# "List all knowledge bases"
```

## Code Standards

### Type Hints (Required: 100% Coverage)

```python
# ✅ Good: Complete type hints
def validate_id(value: str, max_length: int = 255) -> str:
    """Validate ID format."""
    if not value or len(value) > max_length:
        raise ValidationError(f"Invalid ID: {value}")
    return value

# ❌ Bad: Missing type hints
def validate_id(value, max_length=255):
    if not value or len(value) > max_length:
        raise ValidationError(f"Invalid ID: {value}")
    return value
```

### Docstrings (Required: Google-style)

```python
# ✅ Good: Complete Google-style docstring
def execute(self, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute tool operation.

    Args:
        arguments: Tool input parameters with limit and offset

    Returns:
        Tool result as dict with data and pagination info

    Raises:
        ValidationError: If arguments invalid (e.g., limit >1000)
        HTTPError: If API call fails (network, auth, etc.)
    """
    pass

# ❌ Bad: Missing or incomplete docstring
def execute(self, arguments):
    """Execute tool."""
    pass
```

### Modern Python (Required: Python 3.10+ Features)

```python
# ✅ Good: Union operator (Python 3.10+)
def get_value() -> str | None:
    return None

# ❌ Bad: Optional (deprecated style)
from typing import Optional
def get_value() -> Optional[str]:
    return None

# ✅ Good: dict/list built-ins (Python 3.9+)
def process(data: dict[str, Any]) -> list[str]:
    return list(data.keys())

# ❌ Bad: typing.Dict/List (deprecated)
from typing import Dict, List
def process(data: Dict[str, Any]) -> List[str]:
    return list(data.keys())
```

### File Size (Maximum: 200 LOC)

- Keep files focused and small
- Split large files into multiple modules
- Single Responsibility Principle
- Current exception: `client.py` (209 LOC - monolithic HTTP client acceptable)

### Code Formatting

```bash
# Format code with black (line length: 100)
uv run black src/

# Lint code with ruff
uv run ruff check src/

# Type check with mypy (strict mode)
uv run mypy src/
```

### Import Organization

```python
# 1. Standard library
import asyncio
from datetime import datetime
from typing import Any

# 2. Third-party
import httpx
from pydantic import BaseModel, Field

# 3. Local imports (relative)
from ..base import BaseTool
from ...models.chat import Chat
from ...utils.validation import ToolInputValidator
```

### Error Handling

```python
# ✅ Good: Specific exceptions, proper logging
try:
    result = await self.client.get(endpoint)
except ValidationError as e:
    self.logger.error(f"Validation failed: {e}")
    raise
except HTTPError as e:
    self.logger.error(f"API error: {e}", exc_info=True)
    raise

# ❌ Bad: Bare except, no logging
try:
    result = await self.client.get(endpoint)
except:
    pass
```

## Testing Requirements

### Coverage Targets

- **Overall**: >80% coverage required
- **Critical paths**: 100% coverage required
  - Input validation (`utils/validation.py`)
  - Error sanitization (`utils/error_handler.py`)
  - Rate limiting (`utils/rate_limiter.py`)
  - Exceptions (`exceptions.py`)

### Test Categories

**Unit Tests** (tests/unit/):
- Fast (<5s for all unit tests)
- Isolated (all dependencies mocked)
- Deterministic (no flaky tests)
- Use fixtures from `conftest.py`

**Integration Tests** (tests/integration/):
- Real API calls (requires Open WebUI running)
- Optional (skipped if unavailable)
- Marked with `@pytest.mark.integration`

### Test Structure

```python
"""Tests for my_tool."""

import pytest
from src.tools.my_tool import MyTool


@pytest.mark.asyncio
async def test_my_tool_definition():
    """Test tool definition schema."""
    # Test code here
    pass


@pytest.mark.asyncio
async def test_my_tool_execute_success():
    """Test successful execution."""
    # Test code here
    pass


@pytest.mark.asyncio
async def test_my_tool_execute_validation_error():
    """Test validation error handling."""
    # Test code here
    pass


@pytest.mark.asyncio
async def test_my_tool_execute_api_error():
    """Test API error handling."""
    # Test code here
    pass
```

### Fixtures

Use shared fixtures from `tests/conftest.py`:

- `mock_config`: Mock configuration
- `mock_client`: Mock OpenWebUIClient
- `mock_rate_limiter`: Mock rate limiter
- `tool_factory`: Tool factory with mocks
- `sample_chat_data`: Sample chat data
- `sample_model_data`: Sample model data
- `paginated_response_factory`: Factory for paginated responses

### Running Tests

```bash
# All tests
uv run pytest

# Unit tests only
uv run pytest -m unit

# Integration tests only
uv run pytest -m integration

# Specific test file
uv run pytest tests/unit/test_config.py

# With coverage
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Coverage threshold check
uv run pytest --cov=src --cov-fail-under=80
```

## Pull Request Process

### 1. Before Creating PR

```bash
# Sync with upstream
git fetch upstream
git rebase upstream/main

# Run all checks
uv run black src/
uv run ruff check src/
uv run mypy src/
uv run pytest

# Verify all pass before proceeding
```

### 2. Commit Message Format

Use conventional commit format:

```
type(scope): brief description

Longer description if needed (optional).

Closes #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Add/update tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance tasks

**Examples**:
```
feat(tools): add knowledge_list tool

Implements knowledge_list tool for listing knowledge bases.
Includes pagination support and input validation.

Closes #42
```

```
fix(rate_limiter): correct token refill calculation

Token bucket was not refilling correctly at high rates.
Fixed time delta calculation.

Fixes #56
```

### 3. PR Checklist

Before submitting PR, ensure:

- [ ] Code follows style guide (black, ruff, mypy pass)
- [ ] All tests pass (`uv run pytest`)
- [ ] New code has tests (coverage >80%)
- [ ] Docstrings added (Google-style)
- [ ] Type hints added (100% coverage)
- [ ] No files >200 LOC (or justified exception)
- [ ] CHANGELOG.md updated (if user-facing change)
- [ ] README.md updated (if new feature)

### 4. PR Template

```markdown
## Description

Brief description of changes.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated (if applicable)
- [ ] All tests pass locally

## Checklist

- [ ] Code follows style guide
- [ ] Docstrings added
- [ ] Type hints complete
- [ ] Coverage >80%
- [ ] README.md updated (if needed)
```

### 5. Review Process

1. **Automated Checks**: CI runs linters, tests, coverage
2. **Code Review**: Maintainer reviews code quality, design
3. **Feedback**: Address review comments, push updates
4. **Approval**: Maintainer approves PR
5. **Merge**: Maintainer merges PR

## Release Process

### Versioning (SemVer)

- **MAJOR**: Breaking API changes (e.g., 1.0.0 → 2.0.0)
- **MINOR**: New features, backward-compatible (e.g., 0.1.0 → 0.2.0)
- **PATCH**: Bug fixes, backward-compatible (e.g., 0.1.0 → 0.1.1)

### Release Steps

1. **Update Version**: Edit `pyproject.toml` version field
2. **Update CHANGELOG**: Document all changes since last release
3. **Create Tag**: `git tag v0.2.0`
4. **Push Tag**: `git push upstream v0.2.0`
5. **Create Release**: GitHub release with changelog

### CHANGELOG Format

```markdown
# Changelog

## [0.2.0] - 2025-01-15

### Added
- Knowledge management tools (knowledge_list, knowledge_get, etc.)
- File management tools (file_list, file_upload, etc.)

### Fixed
- Rate limiter token refill calculation
- Error sanitization for nested exceptions

### Changed
- Updated dependencies to latest versions

## [0.1.0] - 2025-11-24

Initial MVP release with 6 core tools.
```

---

## Questions?

- **Documentation**: [README.md](README.md), [TOOLS.md](TOOLS.md), [FAQ.md](FAQ.md)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

Thank you for contributing!
