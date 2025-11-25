"""HTTP client for Open WebUI API.

Provides unified interface for all API operations with retry, rate limiting,
and error handling.
"""

import httpx
import logging
from typing import Any, AsyncIterator
from src.config import Config
from src.exceptions import (
    HTTPError,
    RateLimitError,
    AuthError,
    NotFoundError,
    ValidationError,
    ServerError
)
from src.utils.rate_limiter import RateLimiter
from src.utils.url_builder import build_url

logger = logging.getLogger(__name__)


class OpenWebUIClient:
    """HTTP client for Open WebUI API.

    Provides GET and streaming operations with automatic rate limiting,
    retry logic, and error transformation.

    Args:
        config: Configuration instance
        rate_limiter: Optional rate limiter instance
    """

    def __init__(
        self,
        config: Config,
        rate_limiter: RateLimiter | None = None
    ) -> None:
        """Initialize client.

        Args:
            config: Configuration instance with required API key
            rate_limiter: Optional rate limiter

        Note:
            API key is required and will be used for all API requests via
            Authorization: Bearer <api_key> header.
        """
        self.config = config
        self.base_url = config.base_url
        self.api_key = config.api_key
        self.timeout = config.OPENWEBUI_TIMEOUT
        self.max_retries = config.OPENWEBUI_MAX_RETRIES
        self.rate_limiter = rate_limiter

        self._client: httpx.AsyncClient | None = None

        logger.info(
            f"OpenWebUIClient initialized for {self.base_url} "
            f"(auth: configured)"
        )

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create HTTP client.

        Returns:
            Configured httpx client
        """
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self._build_headers(),
                timeout=self.timeout,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
            )

        return self._client

    def _build_headers(self) -> dict[str, str]:
        """Build request headers with Bearer token authentication.

        All requests include Authorization header with API key/token.

        Returns:
            Request headers dict with Authorization: Bearer <api_key>
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        return headers

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Perform GET request.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data as dict

        Raises:
            HTTPError: On HTTP errors
        """
        # Apply rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire()

        # Build URL
        url = endpoint if endpoint.startswith("http") else build_url(
            self.base_url,
            endpoint,
            params
        )

        # Merge headers
        request_headers = {**self._build_headers(), **(headers or {})}

        logger.info(f"GET {url}")

        try:
            response = await self.client.get(url, headers=request_headers)
            return self._handle_response(response)

        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise HTTPError("Request timeout", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPError(f"Request failed: {str(e)}", status_code=0)

    async def stream(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None
    ) -> AsyncIterator[str]:
        """Perform streaming request.

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET or POST)
            params: Query parameters
            json_data: JSON request body

        Yields:
            Response chunks as strings

        Raises:
            HTTPError: On HTTP errors
        """
        # Apply rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire()

        # Build URL
        url = endpoint if endpoint.startswith("http") else build_url(
            self.base_url,
            endpoint,
            params
        )

        logger.info(f"STREAM {method} {url}")

        try:
            async with self.client.stream(
                method,
                url,
                json=json_data,
                headers=self._build_headers()
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.strip():
                        yield line

        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            logger.error(f"Stream timeout: {e}")
            raise HTTPError("Stream timeout", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Stream error: {e}")
            raise HTTPError(f"Stream failed: {str(e)}", status_code=0)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle HTTP response.

        Args:
            response: HTTP response object

        Returns:
            Response data as dict

        Raises:
            HTTPError: On non-2xx status
        """
        if response.status_code >= 200 and response.status_code < 300:
            try:
                return response.json()
            except Exception:
                return {"data": response.text}

        # Transform error response
        raise self._transform_http_error_from_response(response)

    def _transform_http_error(self, error: httpx.HTTPStatusError) -> HTTPError:
        """Transform httpx error to custom exception.

        Args:
            error: HTTP status error

        Returns:
            Custom HTTPError subclass
        """
        return self._transform_http_error_from_response(error.response)

    def _transform_http_error_from_response(
        self,
        response: httpx.Response
    ) -> HTTPError:
        """Transform response to custom exception.

        Args:
            response: HTTP response

        Returns:
            Custom HTTPError subclass
        """
        status_code = response.status_code

        # Extract error message
        try:
            error_data = response.json()
            message = error_data.get("error", error_data.get("message", response.text))
        except Exception:
            message = response.text or f"HTTP {status_code}"

        # Map to appropriate exception
        if status_code == 400:
            return ValidationError(message)
        elif status_code == 401:
            return AuthError(message, status_code=401)
        elif status_code == 403:
            return AuthError(message, status_code=403)
        elif status_code == 404:
            return NotFoundError(message)
        elif status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            return RateLimitError(message, retry_after=retry_after)
        elif status_code >= 500:
            return ServerError(message, status_code=status_code)
        else:
            return HTTPError(message, status_code=status_code)

    async def close(self) -> None:
        """Close HTTP client and release resources."""
        if self._client:
            await self._client.aclose()
            self._client = None
