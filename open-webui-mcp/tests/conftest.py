"""Shared pytest fixtures for all tests.

Provides common fixtures for configuration, clients, tools, and mock data.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.config import Config
from src.services.client import OpenWebUIClient
from src.utils.rate_limiter import RateLimiter
from src.tools.factory import ToolFactory


@pytest.fixture
def mock_config():
    """Create mock configuration for testing.

    Returns:
        Mock Config instance with test values including required API key
    """
    config = Mock(spec=Config)
    config.base_url = "http://localhost:8080"
    config.api_key = "sk-test-key-1234567890abcdef"
    config.OPENWEBUI_API_KEY = "sk-test-key-1234567890abcdef"
    config.OPENWEBUI_TIMEOUT = 30
    config.OPENWEBUI_MAX_RETRIES = 3
    config.OPENWEBUI_RATE_LIMIT = 10
    config.LOG_LEVEL = "INFO"
    config.LOG_FORMAT = "json"
    return config


@pytest.fixture
def real_config(monkeypatch):
    """Create real configuration for integration tests.

    Uses environment variable for API key if available, otherwise uses test key.

    Returns:
        Real Config instance with required API key
    """
    import os
    api_key = os.getenv("OPENWEBUI_API_KEY", "sk-test-key-1234567890abcdef")

    return Config(
        OPENWEBUI_BASE_URL="http://localhost:8080",
        OPENWEBUI_API_KEY=api_key,
        OPENWEBUI_TIMEOUT=30,
        OPENWEBUI_MAX_RETRIES=3,
        OPENWEBUI_RATE_LIMIT=10
    )


@pytest.fixture
def mock_rate_limiter():
    """Create mock rate limiter.

    Returns:
        Mock RateLimiter that always allows requests
    """
    limiter = AsyncMock(spec=RateLimiter)
    limiter.acquire = AsyncMock()
    limiter.try_acquire = AsyncMock(return_value=True)
    return limiter


@pytest.fixture
def mock_client(mock_config, mock_rate_limiter):
    """Create mock OpenWebUI client.

    Returns:
        Mock OpenWebUIClient
    """
    client = Mock(spec=OpenWebUIClient)
    client.config = mock_config
    client.rate_limiter = mock_rate_limiter
    client.get = AsyncMock()
    client.stream = AsyncMock()
    client.close = AsyncMock()
    return client


@pytest.fixture
async def real_client(real_config, mock_rate_limiter):
    """Create real OpenWebUI client for integration tests.

    Yields:
        Real OpenWebUIClient instance
    """
    client = OpenWebUIClient(
        config=real_config,
        rate_limiter=mock_rate_limiter
    )
    yield client
    await client.close()


@pytest.fixture
def tool_factory(mock_config):
    """Create tool factory with mock config.

    Returns:
        ToolFactory instance
    """
    return ToolFactory(config=mock_config)


@pytest.fixture
def mock_httpx_response():
    """Create mock httpx Response.

    Returns:
        Mock Response with common methods
    """
    response = Mock()
    response.status_code = 200
    response.json = Mock(return_value={"data": []})
    response.text = "OK"
    response.headers = {}
    return response


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests.

    Yields:
        Event loop instance
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_chat_data():
    """Sample chat data from OpenAPI spec.

    Returns:
        Dict with realistic chat response
    """
    return {
        "id": "chat-123",
        "user_id": "user-456",
        "title": "Test Chat",
        "created_at": "2025-01-01T12:00:00Z",
        "updated_at": "2025-01-01T12:30:00Z",
        "messages": [],
        "metadata": {
            "tags": ["test"],
            "archived": False
        }
    }


@pytest.fixture
def sample_model_data():
    """Sample model data from OpenAPI spec.

    Returns:
        Dict with realistic model response
    """
    return {
        "id": "llama2:latest",
        "name": "Llama 2",
        "size": 3800000000,
        "digest": "sha256:abc123",
        "created_at": "2025-01-01T10:00:00Z",
        "updated_at": "2025-01-01T10:00:00Z"
    }


@pytest.fixture
def sample_user_data():
    """Sample user data from OpenAPI spec.

    Returns:
        Dict with realistic user response
    """
    return {
        "id": "user-789",
        "email": "test@example.com",
        "name": "Test User",
        "role": "user",
        "created_at": "2024-12-01T00:00:00Z",
        "updated_at": "2024-12-01T00:00:00Z"
    }


@pytest.fixture
def paginated_response_factory():
    """Factory for creating paginated responses.

    Returns:
        Function that creates paginated response
    """
    def create_response(items, total=None, limit=10, offset=0):
        """Create paginated response.

        Args:
            items: List of items
            total: Total count (defaults to len(items))
            limit: Items per page
            offset: Current offset

        Returns:
            Dict with paginated response structure
        """
        if total is None:
            total = len(items)

        return {
            "data": items,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": (offset + limit) < total
        }

    return create_response
