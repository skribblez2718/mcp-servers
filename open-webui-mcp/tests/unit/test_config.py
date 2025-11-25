"""Tests for configuration module.

Tests configuration validation, defaults, and environment variable loading.
"""

import pytest
from src.config import Config
from src.exceptions import ValidationError


class TestConfig:
    """Test configuration validation and defaults."""

    def test_config_with_minimal_required(self):
        """Test config with only required fields."""
        config = Config(OPENWEBUI_BASE_URL="http://localhost:8080")

        assert config.base_url == "http://localhost:8080"
        assert config.OPENWEBUI_API_KEY is None
        assert config.OPENWEBUI_TIMEOUT == 30
        assert config.OPENWEBUI_MAX_RETRIES == 3
        assert config.OPENWEBUI_RATE_LIMIT == 10

    def test_config_base_url_normalization(self):
        """Test base URL trailing slash removal."""
        config = Config(OPENWEBUI_BASE_URL="http://localhost:8080/")

        assert config.base_url == "http://localhost:8080"
        assert not config.base_url.endswith("/")

    def test_config_with_all_fields(self):
        """Test config with all fields specified."""
        config = Config(
            OPENWEBUI_BASE_URL="https://api.example.com",
            OPENWEBUI_API_KEY="test-key-123",
            OPENWEBUI_TIMEOUT=60,
            OPENWEBUI_MAX_RETRIES=5,
            OPENWEBUI_RATE_LIMIT=20,
            LOG_LEVEL="DEBUG",
            LOG_FORMAT="text"
        )

        assert config.base_url == "https://api.example.com"
        assert config.OPENWEBUI_API_KEY == "test-key-123"
        assert config.OPENWEBUI_TIMEOUT == 60
        assert config.OPENWEBUI_MAX_RETRIES == 5
        assert config.OPENWEBUI_RATE_LIMIT == 20
        assert config.LOG_LEVEL == "DEBUG"
        assert config.LOG_FORMAT == "text"

    def test_config_invalid_base_url_protocol(self):
        """Test config rejects non-HTTP URLs."""
        with pytest.raises(ValidationError, match="must start with http"):
            Config(OPENWEBUI_BASE_URL="ftp://localhost:8080")

    def test_config_invalid_timeout(self):
        """Test config rejects invalid timeout."""
        with pytest.raises(ValidationError, match="OPENWEBUI_TIMEOUT"):
            Config(
                OPENWEBUI_BASE_URL="http://localhost:8080",
                OPENWEBUI_TIMEOUT=0
            )

    def test_config_invalid_max_retries(self):
        """Test config rejects negative max retries."""
        with pytest.raises(ValidationError, match="OPENWEBUI_MAX_RETRIES"):
            Config(
                OPENWEBUI_BASE_URL="http://localhost:8080",
                OPENWEBUI_MAX_RETRIES=-1
            )

    def test_config_invalid_rate_limit(self):
        """Test config rejects invalid rate limit."""
        with pytest.raises(ValidationError, match="OPENWEBUI_RATE_LIMIT"):
            Config(
                OPENWEBUI_BASE_URL="http://localhost:8080",
                OPENWEBUI_RATE_LIMIT=0
            )

    def test_config_https_url(self):
        """Test config accepts HTTPS URLs."""
        config = Config(OPENWEBUI_BASE_URL="https://secure.example.com")

        assert config.base_url == "https://secure.example.com"

    def test_config_defaults_match_specification(self):
        """Test default values match specification."""
        config = Config(OPENWEBUI_BASE_URL="http://localhost:8080")

        # Verify defaults from specification
        assert config.OPENWEBUI_TIMEOUT == 30, "Default timeout should be 30s"
        assert config.OPENWEBUI_MAX_RETRIES == 3, "Default retries should be 3"
        assert config.OPENWEBUI_RATE_LIMIT == 10, "Default rate should be 10 req/s"
        assert config.LOG_LEVEL == "INFO", "Default log level should be INFO"
        assert config.LOG_FORMAT == "json", "Default format should be json"
