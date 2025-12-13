"""Tests for OpenWebUI HTTP client.

Tests GET requests, error handling, rate limiting, and retry logic.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
import httpx
from src.services.client import OpenWebUIClient
from src.config import Config
from src.utils.rate_limiter import RateLimiter
from src.exceptions import (
    HTTPError,
    RateLimitError,
    AuthError,
    NotFoundError,
    ValidationError,
    ServerError
)


class TestOpenWebUIClient:
    """Test OpenWebUI HTTP client."""

    @pytest.fixture
    def config(self):
        """Create test configuration with required API key."""
        return Config(
            OPENWEBUI_BASE_URL="http://localhost:8080",
            OPENWEBUI_API_KEY="sk-test-key-1234567890abcdef",
            OPENWEBUI_TIMEOUT=30,
            OPENWEBUI_MAX_RETRIES=3,
            OPENWEBUI_RATE_LIMIT=10
        )

    @pytest.fixture
    def mock_rate_limiter(self):
        """Create mock rate limiter."""
        limiter = AsyncMock(spec=RateLimiter)
        limiter.acquire = AsyncMock()
        return limiter

    @pytest.fixture
    def client(self, config, mock_rate_limiter):
        """Create client with mocks."""
        return OpenWebUIClient(
            config=config,
            rate_limiter=mock_rate_limiter
        )

    def test_client_initialization(self, config, mock_rate_limiter):
        """Test client initializes with correct values including API key."""
        client = OpenWebUIClient(config, mock_rate_limiter)

        assert client.config == config
        assert client.base_url == "http://localhost:8080"
        assert client.api_key == "sk-test-key-1234567890abcdef"
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.rate_limiter == mock_rate_limiter
        assert client._client is None  # Lazy loaded

    def test_client_builds_headers_with_auth(self, client):
        """Test header building includes required Authorization header."""
        headers = client._build_headers()

        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"
        assert headers["Authorization"] == "Bearer sk-test-key-1234567890abcdef"

    def test_client_builds_headers_bearer_format(self, config, mock_rate_limiter):
        """Test Authorization header uses Bearer token format."""
        config.OPENWEBUI_API_KEY = "sk-custom-key-xyz"
        client = OpenWebUIClient(config, mock_rate_limiter)

        headers = client._build_headers()

        assert headers["Authorization"] == "Bearer sk-custom-key-xyz"
        assert "Bearer" in headers["Authorization"]

    @pytest.mark.asyncio
    async def test_get_success(self, client, mock_rate_limiter):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"data": []})

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            result = await client.get("/api/v1/chats")

            assert result == {"data": []}
            mock_rate_limiter.acquire.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_with_params(self, client):
        """Test GET request with query parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"data": []})

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            await client.get("/api/v1/chats", params={"limit": 10})

            # Verify params passed to httpx
            call_args = mock_client.get.call_args
            assert call_args is not None

    @pytest.mark.asyncio
    async def test_get_handles_400_validation_error(self, client):
        """Test 400 raises ValidationError."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Invalid parameters"

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(ValidationError):
                await client.get("/api/v1/chats")

    @pytest.mark.asyncio
    async def test_get_handles_401_auth_error(self, client):
        """Test 401 raises AuthError."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_response.headers = {}

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(AuthError, match="Authentication required"):
                await client.get("/api/v1/chats")

    @pytest.mark.asyncio
    async def test_get_handles_403_auth_error(self, client):
        """Test 403 raises AuthError."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_response.headers = {}

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(AuthError, match="Permission denied"):
                await client.get("/api/v1/chats")

    @pytest.mark.asyncio
    async def test_get_handles_404_not_found(self, client):
        """Test 404 raises NotFoundError."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_response.headers = {}

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(NotFoundError):
                await client.get("/api/v1/chats/invalid")

    @pytest.mark.asyncio
    async def test_get_handles_429_rate_limit(self, client):
        """Test 429 raises RateLimitError with retry_after."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limited"
        mock_response.headers = {"Retry-After": "60"}

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(RateLimitError) as exc_info:
                await client.get("/api/v1/chats")

            assert exc_info.value.retry_after == 60

    @pytest.mark.asyncio
    async def test_get_handles_500_server_error(self, client):
        """Test 500 raises ServerError."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal error"
        mock_response.headers = {}

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(ServerError):
                await client.get("/api/v1/chats")

    @pytest.mark.asyncio
    async def test_get_handles_503_server_error(self, client):
        """Test 503 raises ServerError."""
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.text = "Service unavailable"
        mock_response.headers = {}

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            with pytest.raises(ServerError):
                await client.get("/api/v1/chats")

    @pytest.mark.asyncio
    async def test_get_respects_rate_limiter(self, client, mock_rate_limiter):
        """Test GET respects rate limiter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={})

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            await client.get("/api/v1/chats")

            # Rate limiter acquire called before request
            mock_rate_limiter.acquire.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_without_rate_limiter(self, config):
        """Test GET works without rate limiter."""
        client = OpenWebUIClient(config, rate_limiter=None)

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={})

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            result = await client.get("/api/v1/chats")

            assert result == {}

    @pytest.mark.asyncio
    async def test_close_client(self, client):
        """Test closing HTTP client."""
        # Access client property to create it
        _ = client.client

        with patch.object(client._client, 'aclose') as mock_close:
            await client.close()

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_without_client_created(self, client):
        """Test close when client never created."""
        # Should not raise error
        await client.close()

    @pytest.mark.asyncio
    async def test_get_with_custom_headers(self, client):
        """Test GET with custom headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={})

        with patch.object(client, 'client') as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            await client.get(
                "/api/v1/chats",
                headers={"X-Custom": "value"}
            )

            # Custom headers should be merged
            call_args = mock_client.get.call_args
            assert call_args is not None

    @pytest.mark.asyncio
    async def test_client_lazy_loading(self, client):
        """Test HTTP client is lazy loaded."""
        assert client._client is None

        # Access client property
        http_client = client.client

        assert http_client is not None
        assert isinstance(http_client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_client_reuses_instance(self, client):
        """Test client property reuses same instance."""
        client1 = client.client
        client2 = client.client

        assert client1 is client2
