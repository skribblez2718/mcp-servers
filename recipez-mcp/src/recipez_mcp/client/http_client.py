"""HTTP client for Recipez API with JWT authentication, retry logic, and error mapping.

Provides centralized HTTP communication with:
- Automatic JWT Bearer token injection
- Exponential backoff retry (1s, 2s, 4s) for 5xx errors
- HTTP status code to MCP exception mapping
- Timeout strategy (30s default, 120s AI endpoints)
"""

import asyncio
import time
from typing import Any, Dict, Optional

import httpx

from recipez_mcp.config import get_settings
from recipez_mcp.utils import (
    MCPTimeoutError,
    get_logger,
    log_api_call,
    map_http_status_to_error,
)

logger = get_logger(__name__)


class HTTPClient:
    """HTTP client for Recipez API communication.

    Features:
    - JWT Bearer authentication (automatic header injection)
    - Retry logic with exponential backoff for 5xx errors
    - HTTP error mapping to MCP exceptions
    - Configurable timeouts (default 30s, AI endpoints 120s)
    - Structured logging for all requests
    """

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_BACKOFF_SECONDS = [1, 2, 4]  # Exponential: 1s, 2s, 4s
    RETRY_STATUS_CODES = range(500, 600)  # 5xx errors only

    # Timeout configuration (seconds)
    DEFAULT_TIMEOUT = 30
    AI_ENDPOINT_TIMEOUT = 120

    def __init__(self):
        """Initialize HTTP client with settings from configuration."""
        self.settings = get_settings()
        self.base_url = self.settings.recipez_base_url
        self.auth_headers = self.settings.get_auth_header()

    def _get_timeout(self, endpoint: str) -> int:
        """Determine timeout based on endpoint type.

        AI endpoints (/api/ai/*) get longer timeout due to generation time.

        Args:
            endpoint: API endpoint path

        Returns:
            Timeout in seconds
        """
        if "/api/ai/" in endpoint:
            return self.AI_ENDPOINT_TIMEOUT
        return self.DEFAULT_TIMEOUT

    async def request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout_override: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic and error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path (e.g., "/api/recipe/all")
            json: JSON request body (for JSON content type)
            data: Form data request body (for multipart/form-data)
            files: Files to upload (for multipart/form-data)
            timeout_override: Override default timeout (seconds)

        Returns:
            Response JSON as dictionary

        Raises:
            MCPAuthError: 401 authentication failure
            MCPForbiddenError: 403 insufficient permissions
            MCPNotFoundError: 404 resource not found
            MCPValidationError: 400 bad request
            MCPRateLimitError: 429 rate limit exceeded
            MCPInternalError: 5xx server error (after retries)
            MCPTimeoutError: Request timeout
        """
        url = f"{self.base_url}{endpoint}"
        timeout = timeout_override or self._get_timeout(endpoint)
        start_time = time.time()

        # Prepare headers
        headers = self.auth_headers.copy()

        # Retry loop
        last_exception = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        json=json,
                        data=data,
                        files=files,
                        headers=headers,
                    )

                    duration_ms = int((time.time() - start_time) * 1000)

                    # Log API call
                    log_api_call(
                        logger,
                        method=method,
                        endpoint=endpoint,
                        status_code=response.status_code,
                        duration_ms=duration_ms,
                        attempt=attempt,
                    )

                    # Success: 2xx responses
                    if 200 <= response.status_code < 300:
                        return response.json()

                    # Client errors (4xx): No retry, fail fast
                    if 400 <= response.status_code < 500:
                        error_data = response.json().get("response", {})
                        error_message = error_data.get(
                            "error", f"HTTP {response.status_code}"
                        )
                        raise map_http_status_to_error(
                            response.status_code, error_message
                        )

                    # Server errors (5xx): Retry with backoff
                    if response.status_code in self.RETRY_STATUS_CODES:
                        error_data = response.json().get("response", {})
                        error_message = error_data.get(
                            "error", f"HTTP {response.status_code}"
                        )

                        if attempt < self.MAX_RETRIES:
                            backoff = self.RETRY_BACKOFF_SECONDS[attempt - 1]
                            logger.warning(
                                f"Server error (attempt {attempt}/{self.MAX_RETRIES}), "
                                f"retrying in {backoff}s",
                                extra={
                                    "endpoint": endpoint,
                                    "status_code": response.status_code,
                                    "backoff_seconds": backoff,
                                },
                            )
                            await asyncio.sleep(backoff)
                            continue
                        else:
                            # Max retries exceeded
                            raise map_http_status_to_error(
                                response.status_code, error_message
                            )

                    # Unexpected status code
                    raise map_http_status_to_error(
                        response.status_code, f"Unexpected status: {response.status_code}"
                    )

            except httpx.TimeoutException as e:
                logger.error(
                    f"Request timeout after {timeout}s",
                    extra={"endpoint": endpoint, "timeout": timeout},
                )
                raise MCPTimeoutError(
                    f"Request timeout after {timeout}s", timeout_seconds=timeout
                ) from e

            except httpx.NetworkError as e:
                # Network errors: retry once, then fail
                if attempt < 2:
                    logger.warning(
                        f"Network error (attempt {attempt}/{self.MAX_RETRIES}), retrying",
                        extra={"endpoint": endpoint, "error": str(e)},
                    )
                    await asyncio.sleep(1)
                    last_exception = e
                    continue
                else:
                    logger.error(
                        "Network error after retry",
                        extra={"endpoint": endpoint, "error": str(e)},
                    )
                    raise map_http_status_to_error(
                        503, f"Network error: {str(e)}"
                    ) from e

        # Should not reach here, but handle gracefully
        if last_exception:
            raise map_http_status_to_error(
                500, f"Max retries exceeded: {str(last_exception)}"
            )
        raise map_http_status_to_error(500, "Unknown error occurred")

    async def get(self, endpoint: str, timeout_override: Optional[int] = None) -> Dict[str, Any]:
        """Make GET request.

        Args:
            endpoint: API endpoint path
            timeout_override: Override default timeout

        Returns:
            Response JSON
        """
        return await self.request("GET", endpoint, timeout_override=timeout_override)

    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout_override: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Make POST request.

        Args:
            endpoint: API endpoint path
            json: JSON request body
            data: Form data request body
            files: Files to upload
            timeout_override: Override default timeout

        Returns:
            Response JSON
        """
        return await self.request(
            "POST", endpoint, json=json, data=data, files=files, timeout_override=timeout_override
        )

    async def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        timeout_override: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Make PUT request.

        Args:
            endpoint: API endpoint path
            json: JSON request body
            timeout_override: Override default timeout

        Returns:
            Response JSON
        """
        return await self.request("PUT", endpoint, json=json, timeout_override=timeout_override)

    async def delete(self, endpoint: str, timeout_override: Optional[int] = None) -> Dict[str, Any]:
        """Make DELETE request.

        Args:
            endpoint: API endpoint path
            timeout_override: Override default timeout

        Returns:
            Response JSON
        """
        return await self.request("DELETE", endpoint, timeout_override=timeout_override)
