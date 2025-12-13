"""Configuration settings for Recipez MCP server.

Loads environment variables with validation using pydantic-settings.
All secrets (JWT token) stored in environment variables only.
"""

from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Required:
        RECIPEZ_BASE_URL: API base URL (e.g., http://localhost:3000)
        RECIPEZ_JWT_TOKEN: JWT Bearer token for authentication

    Optional:
        HOST: Server bind address (default: 0.0.0.0)
        PORT: Server listen port (default: 8000)
        LOG_LEVEL: Logging verbosity (default: INFO)
        CORS_ORIGINS: CORS allowed origins (default: *)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Required settings
    recipez_base_url: str = Field(
        ...,
        description="Recipez API base URL",
    )
    recipez_jwt_token: str = Field(
        ...,
        description="JWT Bearer token for API authentication",
    )

    # Optional settings with defaults
    host: str = Field(
        default="0.0.0.0",
        description="Server bind address",
    )
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Server listen port",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging verbosity (DEBUG|INFO|WARN|ERROR)",
    )
    cors_origins: str = Field(
        default="*",
        description="CORS allowed origins (comma-separated or *)",
    )

    @field_validator("recipez_base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate base URL format.

        Args:
            v: Base URL string

        Returns:
            Validated URL with trailing slash removed

        Raises:
            ValueError: If URL format is invalid
        """
        if not v:
            raise ValueError("RECIPEZ_BASE_URL is required")

        # Basic URL validation
        if not v.startswith(("http://", "https://")):
            raise ValueError(
                f"RECIPEZ_BASE_URL must start with http:// or https://, got: {v}"
            )

        # Remove trailing slash for consistency
        return v.rstrip("/")

    @field_validator("recipez_jwt_token")
    @classmethod
    def validate_jwt_token(cls, v: str) -> str:
        """Validate JWT token is non-empty.

        Args:
            v: JWT token string

        Returns:
            Validated token

        Raises:
            ValueError: If token is empty
        """
        if not v or not v.strip():
            raise ValueError("RECIPEZ_JWT_TOKEN is required and must be non-empty")
        return v.strip()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is valid.

        Args:
            v: Log level string

        Returns:
            Uppercase log level

        Raises:
            ValueError: If log level is invalid
        """
        valid_levels = {"DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()

        if v_upper not in valid_levels:
            raise ValueError(
                f"LOG_LEVEL must be one of {valid_levels}, got: {v}"
            )

        # Normalize WARN to WARNING
        return "WARNING" if v_upper == "WARN" else v_upper

    @property
    def cors_origins_list(self) -> list:
        """Get CORS origins as list.

        Returns:
            List of allowed origins, or ["*"] for all origins
        """
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    def get_auth_header(self) -> dict:
        """Get Authorization header with JWT token.

        Returns:
            Dict with Authorization header
        """
        return {"Authorization": f"Bearer {self.recipez_jwt_token}"}


# Global settings instance (lazy-loaded)
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings singleton.

    Returns:
        Settings instance

    Raises:
        ValueError: If required environment variables are missing
    """
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore
    return _settings


def reload_settings() -> Settings:
    """Force reload settings from environment.

    Useful for testing or runtime configuration updates.

    Returns:
        New Settings instance
    """
    global _settings
    _settings = Settings()  # type: ignore
    return _settings
