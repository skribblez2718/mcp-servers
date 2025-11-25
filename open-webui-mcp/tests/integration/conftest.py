"""Integration test fixtures.

Fixtures for testing against local Open WebUI instance.
"""

import pytest
import httpx
import os


@pytest.fixture(scope="session")
def local_webui_available():
    """Check if local Open WebUI instance is available.

    Returns:
        bool: True if local instance running
    """
    try:
        response = httpx.get(
            "http://localhost:8080/api/health",
            timeout=2.0
        )
        return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        return False


@pytest.fixture
def skip_if_no_local_webui(local_webui_available):
    """Skip test if local Open WebUI not available."""
    if not local_webui_available:
        pytest.skip("Local Open WebUI instance not available")


@pytest.fixture
def integration_config():
    """Configuration for integration tests.

    Uses environment variables or defaults to localhost.
    """
    from src.config import Config

    return Config(
        OPENWEBUI_BASE_URL=os.getenv(
            "OPENWEBUI_BASE_URL",
            "http://localhost:8080"
        ),
        OPENWEBUI_API_KEY=os.getenv("OPENWEBUI_API_KEY"),
        OPENWEBUI_TIMEOUT=30,
        OPENWEBUI_MAX_RETRIES=3,
        OPENWEBUI_RATE_LIMIT=5  # Lower for integration tests
    )
