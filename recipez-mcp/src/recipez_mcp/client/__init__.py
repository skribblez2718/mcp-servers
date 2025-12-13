"""HTTP client package for Recipez API communication.

Provides HTTPClient class with JWT authentication, retry logic, and error mapping.
"""

from recipez_mcp.client.http_client import HTTPClient

__all__ = ["HTTPClient"]
