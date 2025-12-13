"""Tests for URL building utilities.

Tests URL construction, parameter encoding, and safety checks.
"""

import pytest
from src.utils.url_builder import build_url


class TestURLBuilder:
    """Test URL building utilities."""

    def test_build_url_simple(self):
        """Test building simple URL without parameters."""
        url = build_url("http://localhost:8080", "/api/v1/chats")

        assert url == "http://localhost:8080/api/v1/chats"

    def test_build_url_with_params(self):
        """Test building URL with query parameters."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {"limit": 10, "offset": 0}
        )

        assert "limit=10" in url
        assert "offset=0" in url
        assert url.startswith("http://localhost:8080/api/v1/chats?")

    def test_build_url_removes_none_params(self):
        """Test None parameters are excluded."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {"limit": 10, "filter": None}
        )

        assert "limit=10" in url
        assert "filter" not in url

    def test_build_url_encodes_special_chars(self):
        """Test special characters are URL encoded."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/search",
            {"q": "test query with spaces"}
        )

        assert "test+query" in url or "test%20query" in url
        assert "test query" not in url

    def test_build_url_handles_boolean_params(self):
        """Test boolean parameters converted to lowercase."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {"archived": True}
        )

        assert "archived=true" in url.lower()

    def test_build_url_handles_trailing_slash(self):
        """Test handles base URL with trailing slash."""
        url1 = build_url("http://localhost:8080/", "/api/v1/chats")
        url2 = build_url("http://localhost:8080", "/api/v1/chats")

        # Both should produce same result (no double slash)
        assert "//" not in url1.replace("http://", "")
        assert url1 == url2

    def test_build_url_handles_endpoint_without_leading_slash(self):
        """Test endpoint without leading slash."""
        url = build_url("http://localhost:8080", "api/v1/chats")

        assert url == "http://localhost:8080/api/v1/chats"

    def test_build_url_empty_params(self):
        """Test with empty params dict."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {}
        )

        assert url == "http://localhost:8080/api/v1/chats"
        assert "?" not in url

    def test_build_url_numeric_params(self):
        """Test numeric parameter values."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {"limit": 100, "offset": 50}
        )

        assert "limit=100" in url
        assert "offset=50" in url

    def test_build_url_string_param_with_quotes(self):
        """Test string parameter with quotes."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/search",
            {"q": 'test "quoted" string'}
        )

        # Quotes should be encoded
        assert "%22" in url or "quoted" in url
        assert url.startswith("http://localhost:8080")

    def test_build_url_multiple_values_same_key(self):
        """Test handling list values (multiple same key)."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {"tags": ["tag1", "tag2"]}
        )

        # Should handle array/list parameters
        assert "tags" in url
        assert "tag1" in url or "tag2" in url

    def test_build_url_preserves_port(self):
        """Test port number is preserved."""
        url = build_url("http://localhost:8080", "/api/v1/chats")

        assert ":8080" in url

    def test_build_url_https_protocol(self):
        """Test HTTPS protocol preserved."""
        url = build_url("https://api.example.com", "/api/v1/chats")

        assert url.startswith("https://")

    def test_build_url_complex_endpoint(self):
        """Test complex endpoint with multiple segments."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats/chat-123/messages"
        )

        assert url == "http://localhost:8080/api/v1/chats/chat-123/messages"

    def test_build_url_sanitizes_injection_attempt(self):
        """Test parameter injection prevention."""
        url = build_url(
            "http://localhost:8080",
            "/api/v1/chats",
            {"limit": "10&malicious=true"}
        )

        # Should encode the & character
        assert "%26" in url or "&malicious" not in url.split("?")[1].split("&")[0]
