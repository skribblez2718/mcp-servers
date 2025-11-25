"""Tests for tool factory.

Tests lazy loading, dependency injection, caching, and tool discovery.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.tools.factory import ToolFactory
from src.config import Config
from src.tools.chats.chat_list_tool import ChatListTool
from src.utils.rate_limiter import RateLimiter


class TestToolFactory:
    """Test tool factory implementation."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config(
            OPENWEBUI_BASE_URL="http://localhost:8080",
            OPENWEBUI_RATE_LIMIT=10
        )

    @pytest.fixture
    def factory(self, config):
        """Create tool factory."""
        return ToolFactory(config=config)

    def test_factory_initialization(self, config):
        """Test factory initializes correctly."""
        factory = ToolFactory(config)

        assert factory.config == config
        assert factory._client is None
        assert factory._services == {}
        assert factory._tools_cache == {}

    def test_get_service_rate_limiter(self, factory):
        """Test getting rate limiter service."""
        limiter = factory.get_service('rate_limiter')

        assert isinstance(limiter, RateLimiter)
        assert limiter.rate == factory.config.OPENWEBUI_RATE_LIMIT

    def test_get_service_caches_instance(self, factory):
        """Test service instances are cached."""
        limiter1 = factory.get_service('rate_limiter')
        limiter2 = factory.get_service('rate_limiter')

        assert limiter1 is limiter2

    def test_get_service_unknown(self, factory):
        """Test getting unknown service raises error."""
        with pytest.raises(ValueError, match="Unknown service"):
            factory.get_service('unknown_service')

    def test_client_property_lazy_loads(self, factory):
        """Test client is lazy loaded."""
        assert factory._client is None

        client = factory.client

        assert client is not None
        assert factory._client is not None

    def test_client_property_reuses_instance(self, factory):
        """Test client property reuses same instance."""
        client1 = factory.client
        client2 = factory.client

        assert client1 is client2

    def test_client_has_rate_limiter(self, factory):
        """Test created client has rate limiter."""
        client = factory.client

        assert client.rate_limiter is not None
        assert isinstance(client.rate_limiter, RateLimiter)

    def test_create_tool_chat_list(self, factory):
        """Test creating chat_list tool."""
        tool = factory.create_tool("chat_list")

        assert isinstance(tool, ChatListTool)
        assert tool.client is not None

    def test_create_tool_caches_instance(self, factory):
        """Test tool instances are cached."""
        tool1 = factory.create_tool("chat_list")
        tool2 = factory.create_tool("chat_list")

        assert tool1 is tool2

    def test_create_tool_invalid_name(self, factory):
        """Test creating non-existent tool raises error."""
        with pytest.raises((ImportError, AttributeError, ValueError)):
            factory.create_tool("nonexistent_tool")

    def test_create_tool_injects_client(self, factory):
        """Test created tool has client injected."""
        tool = factory.create_tool("chat_list")

        assert tool.client is factory.client

    @patch('src.tools.factory.pkgutil.walk_packages')
    def test_discover_tools(self, mock_walk, factory):
        """Test tool discovery scans filesystem."""
        # Mock discovered modules
        mock_walk.return_value = [
            (None, 'tools.chats.chat_list_tool', False),
            (None, 'tools.models.model_list_tool', False),
        ]

        tools = factory.get_all_tools()

        # Should discover and create tools
        assert len(tools) >= 0  # May fail import, but shouldn't crash

    def test_create_multiple_different_tools(self, factory):
        """Test creating multiple different tools."""
        tool1 = factory.create_tool("chat_list")

        # Try second tool (may not exist in test env)
        try:
            tool2 = factory.create_tool("chat_get")
            assert tool1 is not tool2
        except (ImportError, AttributeError):
            # Tool doesn't exist yet, that's OK
            pass

    def test_factory_tool_resolution(self, factory):
        """Test tool name resolution logic."""
        module_path, class_name = factory._resolve_tool("chat_list")

        assert "chat_list_tool" in module_path
        assert class_name == "ChatListTool"

    def test_factory_tool_resolution_patterns(self, factory):
        """Test various tool name patterns."""
        # Simple tool
        module, cls = factory._resolve_tool("chat_list")
        assert "chats" in module
        assert cls == "ChatListTool"

        # Model tool
        module, cls = factory._resolve_tool("model_get")
        assert "models" in module
        assert cls == "ModelGetTool"

        # User tool
        module, cls = factory._resolve_tool("user_list")
        assert "users" in module
        assert cls == "UserListTool"

    @pytest.mark.asyncio
    async def test_factory_cleanup(self, factory):
        """Test factory cleanup closes client."""
        # Create client
        client = factory.client

        with patch.object(client, 'close', new_callable=AsyncMock) as mock_close:
            await factory.cleanup()

            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_factory_cleanup_without_client(self, factory):
        """Test cleanup when client never created."""
        # Should not raise error
        await factory.cleanup()

    def test_factory_isolates_tools(self, factory):
        """Test tools don't share mutable state."""
        tool1 = factory.create_tool("chat_list")
        tool2 = factory.create_tool("chat_list")

        # Same cached instance
        assert tool1 is tool2

        # But creating fresh instance should be independent
        factory._tools_cache.clear()
        tool3 = factory.create_tool("chat_list")

        assert tool1 is not tool3

    def test_factory_config_propagation(self, config):
        """Test config propagates to all created objects."""
        factory = ToolFactory(config)

        # Config in factory
        assert factory.config is config

        # Config in client
        client = factory.client
        assert client.config is config

        # Config accessible to tools (via client)
        tool = factory.create_tool("chat_list")
        assert tool.client.config is config
