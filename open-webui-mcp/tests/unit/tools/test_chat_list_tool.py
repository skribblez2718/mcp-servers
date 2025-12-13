"""Tests for chat list tool.

Tests input validation, API calls, response transformation, and error handling.
"""

import pytest
from unittest.mock import AsyncMock, Mock
from src.tools.chats.chat_list_tool import ChatListTool
from src.exceptions import ValidationError, NotFoundError, RateLimitError
from tests.fixtures.openapi_responses import OpenAPIResponses


class TestChatListTool:
    """Test chat list tool."""

    @pytest.fixture
    def mock_client(self):
        """Create mock client."""
        client = Mock()
        client.get = AsyncMock()
        return client

    @pytest.fixture
    def tool(self, mock_client):
        """Create chat list tool."""
        return ChatListTool(client=mock_client)

    def test_get_definition(self, tool):
        """Test tool definition structure."""
        definition = tool.get_definition()

        assert definition["name"] == "chat_list"
        assert "description" in definition
        assert "inputSchema" in definition
        assert definition["inputSchema"]["type"] == "object"

        # Check parameters
        props = definition["inputSchema"]["properties"]
        assert "limit" in props
        assert "offset" in props
        assert "archived" in props

        # Check limit constraints
        assert props["limit"]["minimum"] == 1
        assert props["limit"]["maximum"] == 1000

    @pytest.mark.asyncio
    async def test_execute_with_default_params(self, tool, mock_client):
        """Test execute with default parameters."""
        mock_client.get.return_value = OpenAPIResponses.chat_list(3)

        result = await tool.execute({})

        # Verify API call
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/api/v1/chats"

        # Verify result structure
        assert "chats" in result
        assert "total" in result
        assert "limit" in result
        assert "offset" in result
        assert len(result["chats"]) == 3

    @pytest.mark.asyncio
    async def test_execute_with_custom_pagination(self, tool, mock_client):
        """Test execute with custom limit and offset."""
        mock_client.get.return_value = OpenAPIResponses.chat_list(5)

        result = await tool.execute({"limit": 20, "offset": 10})

        # Verify pagination params
        call_args = mock_client.get.call_args
        params = call_args[1]["params"]
        assert params["limit"] == 20
        assert params["offset"] == 10

    @pytest.mark.asyncio
    async def test_execute_with_archived_filter(self, tool, mock_client):
        """Test execute with archived filter."""
        mock_client.get.return_value = OpenAPIResponses.chat_list(2)

        result = await tool.execute({"archived": True})

        # Verify archived param
        call_args = mock_client.get.call_args
        params = call_args[1]["params"]
        assert params["archived"] == "true"

    @pytest.mark.asyncio
    async def test_execute_validates_limit_too_small(self, tool):
        """Test validation error for limit < 1."""
        with pytest.raises(ValidationError, match="between 1 and 1000"):
            await tool.execute({"limit": 0})

    @pytest.mark.asyncio
    async def test_execute_validates_limit_too_large(self, tool):
        """Test validation error for limit > 1000."""
        with pytest.raises(ValidationError, match="between 1 and 1000"):
            await tool.execute({"limit": 1001})

    @pytest.mark.asyncio
    async def test_execute_validates_offset_negative(self, tool):
        """Test validation error for negative offset."""
        with pytest.raises(ValidationError, match="offset must be >= 0"):
            await tool.execute({"offset": -1})

    @pytest.mark.asyncio
    async def test_execute_handles_empty_response(self, tool, mock_client):
        """Test handling empty chat list."""
        mock_client.get.return_value = OpenAPIResponses.chat_list(0)

        result = await tool.execute({})

        assert result["chats"] == []
        assert result["total"] == 0

    @pytest.mark.asyncio
    async def test_execute_handles_api_error(self, tool, mock_client):
        """Test handling API errors."""
        mock_client.get.side_effect = NotFoundError("Endpoint not found")

        with pytest.raises(NotFoundError):
            await tool.execute({})

    @pytest.mark.asyncio
    async def test_execute_handles_rate_limit(self, tool, mock_client):
        """Test handling rate limit errors."""
        mock_client.get.side_effect = RateLimitError(
            "Rate limited",
            retry_after=60
        )

        with pytest.raises(RateLimitError) as exc_info:
            await tool.execute({})

        assert exc_info.value.retry_after == 60

    @pytest.mark.asyncio
    async def test_execute_transforms_response_format(self, tool, mock_client):
        """Test response transformation handles different formats."""
        # Test with "data" key
        mock_client.get.return_value = {
            "data": [{"id": "chat-1"}],
            "total": 1,
            "limit": 10,
            "offset": 0,
            "has_next": False
        }

        result = await tool.execute({})
        assert result["chats"] == [{"id": "chat-1"}]

        # Test with "chats" key (alternative format)
        mock_client.get.return_value = {
            "chats": [{"id": "chat-2"}],
            "total": 1
        }

        result = await tool.execute({})
        assert result["chats"] == [{"id": "chat-2"}]

    @pytest.mark.asyncio
    async def test_execute_pagination_has_next(self, tool, mock_client):
        """Test has_next calculation."""
        mock_client.get.return_value = {
            "data": [{"id": f"chat-{i}"} for i in range(10)],
            "total": 50,
            "limit": 10,
            "offset": 0,
            "has_next": True
        }

        result = await tool.execute({"limit": 10, "offset": 0})

        assert result["has_next"] is True

    @pytest.mark.asyncio
    async def test_execute_validates_param_types(self, tool):
        """Test validation of parameter types."""
        with pytest.raises(ValidationError):
            await tool.execute({"limit": "not_an_int"})

    @pytest.mark.asyncio
    async def test_execute_ignores_extra_params(self, tool, mock_client):
        """Test tool ignores unknown parameters."""
        mock_client.get.return_value = OpenAPIResponses.chat_list(1)

        # Should not raise error for extra param
        result = await tool.execute({"limit": 10, "unknown_param": "value"})

        assert "chats" in result
