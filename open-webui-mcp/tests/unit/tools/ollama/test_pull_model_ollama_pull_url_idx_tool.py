"""Tests for PullModelOllamaPullUrlIdxTool."""

import pytest
from unittest.mock import AsyncMock, Mock
from src.tools.ollama.pull_model_ollama_pull_url_idx_tool import PullModelOllamaPullUrlIdxTool
from src.exceptions import ValidationError, NotFoundError, HTTPError


class TestPullModelOllamaPullUrlIdxTool:
    """Tests for pull_model_ollama_pull_url_idx."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HTTP client."""
        client = Mock()
        client.post = AsyncMock(return_value={})
        return client

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = Mock()
        return config

    @pytest.fixture
    def tool(self, mock_client, mock_config):
        """Create tool instance."""
        return PullModelOllamaPullUrlIdxTool(client=mock_client, config=mock_config)

    def test_get_definition(self, tool):
        """Test tool definition structure."""
        definition = tool.get_definition()

        assert definition["name"] == "pull_model_ollama_pull_url_idx"
        assert "description" in definition
        assert "inputSchema" in definition
        assert definition["inputSchema"]["type"] == "object"

    @pytest.mark.asyncio
    async def test_execute_success(self, tool, mock_client):
        """Test successful execution."""
        mock_client.post.return_value = {"status": "ok"}

        result = await tool.execute({})

        assert result is not None
        mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_not_found(self, tool, mock_client):
        """Test handling of 404 errors."""
        mock_client.post.side_effect = NotFoundError("Not found")

        with pytest.raises(NotFoundError):
            await tool.execute({})

    @pytest.mark.asyncio
    async def test_execute_http_error(self, tool, mock_client):
        """Test handling of HTTP errors."""
        mock_client.post.side_effect = HTTPError("Server error", status_code=500)

        with pytest.raises(HTTPError):
            await tool.execute({})