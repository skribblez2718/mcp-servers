"""Tests for DeleteUserByIdUsersUserIdTool."""

import pytest
from unittest.mock import AsyncMock, Mock
from src.tools.users.delete_user_by_id_users_user_id_tool import DeleteUserByIdUsersUserIdTool
from src.exceptions import ValidationError, NotFoundError, HTTPError


class TestDeleteUserByIdUsersUserIdTool:
    """Tests for delete_user_by_id_users_user_id."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HTTP client."""
        client = Mock()
        client.delete = AsyncMock(return_value={})
        return client

    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = Mock()
        return config

    @pytest.fixture
    def tool(self, mock_client, mock_config):
        """Create tool instance."""
        return DeleteUserByIdUsersUserIdTool(client=mock_client, config=mock_config)

    def test_get_definition(self, tool):
        """Test tool definition structure."""
        definition = tool.get_definition()

        assert definition["name"] == "delete_user_by_id_users_user_id"
        assert "description" in definition
        assert "inputSchema" in definition
        assert definition["inputSchema"]["type"] == "object"

    @pytest.mark.asyncio
    async def test_execute_success(self, tool, mock_client):
        """Test successful execution."""
        mock_client.delete.return_value = {"status": "ok"}

        result = await tool.execute({})

        assert result is not None
        mock_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_not_found(self, tool, mock_client):
        """Test handling of 404 errors."""
        mock_client.delete.side_effect = NotFoundError("Not found")

        with pytest.raises(NotFoundError):
            await tool.execute({})

    @pytest.mark.asyncio
    async def test_execute_http_error(self, tool, mock_client):
        """Test handling of HTTP errors."""
        mock_client.delete.side_effect = HTTPError("Server error", status_code=500)

        with pytest.raises(HTTPError):
            await tool.execute({})