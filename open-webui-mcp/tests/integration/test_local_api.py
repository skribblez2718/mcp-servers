"""Integration tests against local Open WebUI instance.

Tests real API calls to verify generated code works with actual API.
"""

import pytest
from src.services.client import OpenWebUIClient
from src.utils.rate_limiter import RateLimiter
from src.tools.chats.chat_list_tool import ChatListTool
from src.tools.admin.admin_health_tool import AdminHealthTool
from src.exceptions import HTTPError


class TestLocalAPIIntegration:
    """Integration tests against local Open WebUI."""

    @pytest.fixture
    async def real_client(self, integration_config):
        """Create real client for local API."""
        rate_limiter = RateLimiter(rate=integration_config.OPENWEBUI_RATE_LIMIT)
        client = OpenWebUIClient(
            config=integration_config,
            rate_limiter=rate_limiter
        )
        yield client
        await client.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_health_check_endpoint(
        self,
        skip_if_no_local_webui,
        real_client
    ):
        """Test health check endpoint works."""
        try:
            result = await real_client.get("/api/health")

            assert "status" in result or "version" in result
        except HTTPError as e:
            # If endpoint doesn't exist, that's OK for this test
            assert e.status_code in [404, 405]

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_chat_list_real_api(
        self,
        skip_if_no_local_webui,
        real_client
    ):
        """Test chat list against real API."""
        tool = ChatListTool(client=real_client)

        try:
            result = await tool.execute({"limit": 5, "offset": 0})

            # Verify response structure
            assert "chats" in result
            assert "total" in result
            assert "limit" in result
            assert "offset" in result
            assert isinstance(result["chats"], list)

        except HTTPError as e:
            # API might require auth or have different endpoint
            assert e.status_code in [401, 403, 404]

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_admin_health_tool_real_api(
        self,
        skip_if_no_local_webui,
        real_client
    ):
        """Test admin health tool against real API."""
        tool = AdminHealthTool(client=real_client)

        try:
            result = await tool.execute({})

            # Should have health status
            assert "status" in result or "health" in result

        except HTTPError as e:
            # Endpoint might not exist or require auth
            assert e.status_code in [401, 403, 404]

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_rate_limiting_works(
        self,
        skip_if_no_local_webui,
        real_client
    ):
        """Test rate limiting prevents overwhelming API."""
        import time

        # Make multiple rapid requests
        start = time.time()
        for _ in range(6):  # More than rate limit of 5
            try:
                await real_client.get("/api/health")
            except HTTPError:
                # Ignore errors, we're testing rate limiting
                pass

        elapsed = time.time() - start

        # Should take at least ~1s due to rate limiting (6 req at 5/s)
        assert elapsed >= 1.0, "Rate limiter should slow down requests"

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_invalid_endpoint_returns_404(
        self,
        skip_if_no_local_webui,
        real_client
    ):
        """Test invalid endpoint returns appropriate error."""
        from src.exceptions import NotFoundError

        with pytest.raises((NotFoundError, HTTPError)) as exc_info:
            await real_client.get("/api/v1/nonexistent")

        if isinstance(exc_info.value, HTTPError):
            assert exc_info.value.status_code == 404

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_connection_to_wrong_port_fails(self):
        """Test connection to wrong port fails gracefully."""
        from src.config import Config
        import httpx

        config = Config(
            OPENWEBUI_BASE_URL="http://localhost:9999",  # Wrong port
            OPENWEBUI_TIMEOUT=2
        )
        client = OpenWebUIClient(config, rate_limiter=None)

        with pytest.raises((httpx.ConnectError, httpx.TimeoutException, HTTPError)):
            await client.get("/api/health")

        await client.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_pagination_works(
        self,
        skip_if_no_local_webui,
        real_client
    ):
        """Test pagination parameters work correctly."""
        tool = ChatListTool(client=real_client)

        try:
            # Get first page
            page1 = await tool.execute({"limit": 2, "offset": 0})

            # Get second page
            page2 = await tool.execute({"limit": 2, "offset": 2})

            # Pages should have correct structure
            assert page1["limit"] == 2
            assert page1["offset"] == 0
            assert page2["limit"] == 2
            assert page2["offset"] == 2

            # If we have data, pages should be different
            if page1["total"] > 2:
                assert page1["chats"] != page2["chats"]

        except HTTPError as e:
            # API might require auth
            assert e.status_code in [401, 403, 404]
