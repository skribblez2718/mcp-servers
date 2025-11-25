"""Configuration management for Open WebUI MCP Server.

Uses Pydantic Settings for environment variable validation and type safety.
All configuration loaded from environment variables or .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from src.exceptions import ValidationError as CustomValidationError


class Config(BaseSettings):
    """Configuration from environment variables.

    Attributes:
        OPENWEBUI_BASE_URL: Base URL of Open WebUI instance (required)
        OPENWEBUI_API_KEY: Bearer token for API authentication (required)
            Can be either an API key or JWT token from Open WebUI.
            Get from: Open WebUI → Settings → Account → API Keys
        OPENWEBUI_TIMEOUT: HTTP request timeout in seconds
        OPENWEBUI_MAX_RETRIES: Maximum retry attempts
        OPENWEBUI_RATE_LIMIT: Client-side rate limit (requests/second)
        LOG_LEVEL: Logging level
        LOG_FORMAT: Log format (json or text)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # Required
    OPENWEBUI_BASE_URL: str
    OPENWEBUI_API_KEY: str

    # Performance tuning
    OPENWEBUI_TIMEOUT: int = 30
    OPENWEBUI_MAX_RETRIES: int = 3
    OPENWEBUI_RATE_LIMIT: int = 10

    # HTTP Server
    PORT: int = 8000
    HOST: str = "127.0.0.1"

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["json", "text"] = "json"

    def model_post_init(self, __context: object) -> None:
        """Validate configuration after initialization.

        Raises:
            CustomValidationError: If validation fails
        """
        # Normalize base URL (remove trailing slash)
        if self.OPENWEBUI_BASE_URL.endswith("/"):
            object.__setattr__(
                self,
                "OPENWEBUI_BASE_URL",
                self.OPENWEBUI_BASE_URL.rstrip("/")
            )

        # Validate URL format
        if not self.OPENWEBUI_BASE_URL.startswith(("http://", "https://")):
            raise CustomValidationError(
                "OPENWEBUI_BASE_URL must start with http:// or https://"
            )

        # Validate API key is present
        if not self.OPENWEBUI_API_KEY or len(self.OPENWEBUI_API_KEY.strip()) == 0:
            raise CustomValidationError(
                "OPENWEBUI_API_KEY is required. "
                "Get your API key from: Open WebUI → Settings → Account → API Keys"
            )

        # Validate numeric ranges
        if self.OPENWEBUI_TIMEOUT < 1:
            raise CustomValidationError(
                "OPENWEBUI_TIMEOUT must be >= 1"
            )

        if self.OPENWEBUI_MAX_RETRIES < 0:
            raise CustomValidationError(
                "OPENWEBUI_MAX_RETRIES must be >= 0"
            )

        if self.OPENWEBUI_RATE_LIMIT < 1:
            raise CustomValidationError(
                "OPENWEBUI_RATE_LIMIT must be >= 1"
            )

        # Validate HTTP server settings
        if self.PORT < 1 or self.PORT > 65535:
            raise CustomValidationError(
                "PORT must be between 1 and 65535"
            )

    @property
    def base_url(self) -> str:
        """Get normalized base URL without trailing slash.

        Returns:
            Normalized base URL
        """
        return self.OPENWEBUI_BASE_URL.rstrip("/")

    @property
    def api_key(self) -> str:
        """Get API key for authentication.

        Returns:
            API key string

        Note:
            API key is always present due to validation in model_post_init.
        """
        return self.OPENWEBUI_API_KEY
