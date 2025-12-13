"""Tests for GetFunctionsFunctionsTool."""

import pytest
from unittest.mock import AsyncMock, Mock
from src.tools.functions.get_functions_functions_tool import GetFunctionsFunctionsTool
from src.exceptions import ValidationError, NotFoundError, HTTPError


class TestGetFunctionsFunctionsTool:
    """Tests for get_functions_functions."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HTTP client."""
        client = Mock()
        client.get = AsyncMock(return_value={})
        return client

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = Mock()
        return config

    @pytest.fixture
    def tool(self, mock_client, mock_config):
        """Create tool instance."""
        return GetFunctionsFunctionsTool(client=mock_client, config=mock_config)

    def test_get_definition(self, tool):
        """Test tool definition structure."""
        definition = tool.get_definition()

        assert definition["name"] == "get_functions_functions"
        assert "description" in definition
        assert "inputSchema" in definition
        assert definition["inputSchema"]["type"] == "object"

    @pytest.mark.asyncio
    async def test_execute_success(self, tool, mock_client):
        """Test successful execution."""
        mock_client.get.return_value = {"status": "ok"}

        result = await tool.execute({})

        assert result is not None
        mock_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_not_found(self, tool, mock_client):
        """Test handling of 404 errors."""
        mock_client.get.side_effect = NotFoundError("Not found")

        with pytest.raises(NotFoundError):
            await tool.execute({})

    @pytest.mark.asyncio
    async def test_execute_http_error(self, tool, mock_client):
        """Test handling of HTTP errors."""
        mock_client.get.side_effect = HTTPError("Server error", status_code=500)

        with pytest.raises(HTTPError):
            await tool.execute({})