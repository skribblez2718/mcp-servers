"""HTTP client for Open WebUI API.

Provides unified interface for all API operations with retry, rate limiting,
and error handling.
"""

import httpx
import logging
import time
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
        start_time = time.time()

        try:
            response = await self.client.get(url, headers=request_headers)
            duration_ms = (time.time() - start_time) * 1000
            logger.debug(f"GET {url} completed in {duration_ms:.0f}ms (status: {response.status_code})")
            return self._handle_response(response)

        except httpx.HTTPStatusError as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"GET {url} failed in {duration_ms:.0f}ms: HTTP {e.response.status_code}")
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"GET {url} timeout after {duration_ms:.0f}ms: {e}")
            raise HTTPError("Request timeout", status_code=408)
        except httpx.RequestError as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"GET {url} error after {duration_ms:.0f}ms: {e}")
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
        # Log response status for all requests
        logger.debug(
            f"Response: {response.status_code} {response.reason_phrase}",
            extra={"url": str(response.url), "status_code": response.status_code}
        )

        if response.status_code >= 200 and response.status_code < 300:
            try:
                return response.json()
            except Exception:
                return {"data": response.text}

        # Log error response body for debugging (truncate to 500 chars)
        response_preview = response.text[:500] if response.text else "(empty)"
        logger.error(
            f"HTTP {response.status_code} error from {response.url}: {response_preview}",
            extra={
                "status_code": response.status_code,
                "url": str(response.url),
                "response_preview": response_preview
            }
        )

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

    async def post(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Perform POST request with JSON body.

        Args:
            endpoint: API endpoint path
            json_data: JSON request body
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

        logger.info(f"POST {url}")
        start_time = time.time()

        try:
            response = await self.client.post(url, json=json_data, headers=request_headers)
            duration_ms = (time.time() - start_time) * 1000
            logger.debug(f"POST {url} completed in {duration_ms:.0f}ms (status: {response.status_code})")
            return self._handle_response(response)

        except httpx.HTTPStatusError as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"POST {url} failed in {duration_ms:.0f}ms: HTTP {e.response.status_code}")
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"POST {url} timeout after {duration_ms:.0f}ms: {e}")
            raise HTTPError("Request timeout", status_code=408)
        except httpx.RequestError as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"POST {url} error after {duration_ms:.0f}ms: {e}")
            raise HTTPError(f"Request failed: {str(e)}", status_code=0)

    async def put(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Perform PUT request with JSON body.

        Args:
            endpoint: API endpoint path
            json_data: JSON request body
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

        logger.info(f"PUT {url}")

        try:
            response = await self.client.put(url, json=json_data, headers=request_headers)
            return self._handle_response(response)

        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise HTTPError("Request timeout", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPError(f"Request failed: {str(e)}", status_code=0)

    async def patch(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Perform PATCH request with JSON body.

        Args:
            endpoint: API endpoint path
            json_data: JSON request body
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

        logger.info(f"PATCH {url}")

        try:
            response = await self.client.patch(url, json=json_data, headers=request_headers)
            return self._handle_response(response)

        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise HTTPError("Request timeout", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPError(f"Request failed: {str(e)}", status_code=0)

    async def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Perform DELETE request.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data as dict

        Raises:
            HTTPError: On HTTP errors

        Note:
            DELETE requests do not include request body per HTTP spec (RFC 7231).
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

        logger.info(f"DELETE {url}")

        try:
            response = await self.client.delete(url, headers=request_headers)
            return self._handle_response(response)

        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise HTTPError("Request timeout", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPError(f"Request failed: {str(e)}", status_code=0)

    async def post_with_file(
        self,
        endpoint: str,
        file_path: str,
        field_name: str = 'file',
        additional_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """POST with file upload (multipart/form-data).

        Security: Path traversal prevention, symlink blocking, size limits.

        Args:
            endpoint: API endpoint path
            file_path: Path to file to upload
            field_name: Form field name for file (default: 'file')
            additional_data: Additional form fields
            params: Query parameters
            headers: Additional headers

        Returns:
            API response data

        Raises:
            ValidationError: If file invalid, outside allowed directories, or exceeds size
            HTTPError: If upload fails
        """
        from pathlib import Path
        import mimetypes

        # SECURITY FIX AV-001: Canonicalize path to absolute form
        try:
            path = Path(file_path).resolve(strict=True)
        except (OSError, RuntimeError) as e:
            raise ValidationError(f"Invalid file path: {e}")

        # SECURITY FIX AV-001: Block symlinks (prevents reading outside intended directories)
        if path.is_symlink():
            raise ValidationError("Symlink file paths not allowed for security")

        # SECURITY FIX AV-001: Validate file exists (strict=True checks this but explicit for clarity)
        if not path.exists() or not path.is_file():
            raise ValidationError(f"File not found or not a regular file: {file_path}")

        # Validate file size BEFORE reading
        file_size = path.stat().st_size
        max_file_size = getattr(self.config, 'OPENWEBUI_MAX_FILE_SIZE', 10 * 1024 * 1024)
        if file_size > max_file_size:
            max_mb = max_file_size / (1024 * 1024)
            raise ValidationError(f"File exceeds {max_mb:.1f}MB size limit")

        # SECURITY FIX AV-001: Byte-level MIME validation (not just extension)
        try:
            import magic
            detected_mime = magic.from_file(str(path), mime=True)
        except ImportError:
            # Fallback to extension-based MIME if python-magic not available
            logger.warning("python-magic not available, using mimetypes.guess_type()")
            detected_mime, _ = mimetypes.guess_type(str(path))
            detected_mime = detected_mime or 'application/octet-stream'

        # Apply rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire()

        # Build request
        url = endpoint if endpoint.startswith("http") else build_url(
            self.base_url, endpoint, params
        )
        request_headers = {**self._build_headers(), **(headers or {})}
        # Remove Content-Type - httpx sets it for multipart
        request_headers.pop('Content-Type', None)

        logger.info(f"POST (file upload) {url}")

        try:
            with open(path, 'rb') as f:
                files = {field_name: (path.name, f, detected_mime)}
                response = await self.client.post(
                    url,
                    files=files,
                    data=additional_data,
                    headers=request_headers
                )
                return self._handle_response(response)
        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.TimeoutException as e:
            logger.error(f"Upload timeout: {e}")
            raise HTTPError(f"Upload timeout: {e}", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Upload failed: {e}")
            raise HTTPError(f"Upload failed: {e}", status_code=0)

    async def post_streaming(
        self,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float = 30.0
    ) -> dict[str, Any]:
        """POST to streaming endpoint, buffer SSE/JSONL response.

        Security: Buffer size limits to prevent memory exhaustion.

        Args:
            endpoint: API endpoint path
            json_data: Request body JSON
            params: Query parameters
            timeout: Stream timeout in seconds (default: 30)

        Returns:
            Buffered streaming response data

        Raises:
            HTTPError: If stream fails, times out, or exceeds size limit (413)
        """
        import json as json_lib

        # SECURITY FIX AV-002: Maximum streaming response size (prevent OOM)
        MAX_STREAM_SIZE = getattr(
            self.config, 'OPENWEBUI_MAX_STREAM_SIZE', 10 * 1024 * 1024  # 10MB fallback
        )

        if self.rate_limiter:
            await self.rate_limiter.acquire()

        url = endpoint if endpoint.startswith("http") else build_url(
            self.base_url, endpoint, params
        )

        chunks: list[str] = []
        total_size = 0  # SECURITY FIX AV-002: Track cumulative buffer size

        logger.info(f"POST (streaming) {url}")

        try:
            # Use httpx-sse for SSE streaming
            try:
                from httpx_sse import aconnect_sse

                async with aconnect_sse(
                    self.client,
                    "POST",
                    url,
                    json=json_data,
                    headers=self._build_headers(),
                    timeout=timeout
                ) as event_source:
                    async for sse in event_source.aiter_sse():
                        # SECURITY FIX AV-002: Calculate chunk size in bytes
                        chunk_data = sse.data
                        chunk_size = len(chunk_data.encode('utf-8'))
                        total_size += chunk_size

                        # SECURITY FIX AV-002: Fail-fast if buffer limit exceeded
                        if total_size > MAX_STREAM_SIZE:
                            max_mb = MAX_STREAM_SIZE / (1024 * 1024)
                            raise HTTPError(
                                f"Streaming response exceeds {max_mb:.1f}MB buffer limit. "
                                f"Received {total_size / (1024 * 1024):.1f}MB.",
                                status_code=413  # Payload Too Large
                            )

                        chunks.append(chunk_data)

            except ImportError:
                # Fallback to basic streaming if httpx-sse not available
                logger.warning("httpx-sse not available, using basic streaming")
                async with self.client.stream(
                    "POST",
                    url,
                    json=json_data,
                    headers=self._build_headers(),
                    timeout=timeout
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if line.strip():
                            chunk_size = len(line.encode('utf-8'))
                            total_size += chunk_size

                            if total_size > MAX_STREAM_SIZE:
                                max_mb = MAX_STREAM_SIZE / (1024 * 1024)
                                raise HTTPError(
                                    f"Streaming response exceeds {max_mb:.1f}MB buffer limit.",
                                    status_code=413
                                )

                            chunks.append(line.strip())

            # Combine and parse
            combined = ''.join(chunks)

            # Detect format (JSONL vs JSON)
            if '\n' in combined and combined.count('\n') > 1:
                lines = [l.strip() for l in combined.split('\n') if l.strip()]
                return {
                    'streaming_data': [json_lib.loads(l) for l in lines],
                    'format': 'jsonl',
                    'total_bytes': total_size,
                    'chunks_received': len(chunks)
                }
            else:
                parsed = json_lib.loads(combined) if combined else {}
                return {
                    **parsed,
                    'total_bytes': total_size,
                    'chunks_received': len(chunks)
                }

        except httpx.TimeoutException as e:
            logger.error(f"Stream timeout after {timeout}s: {e}")
            raise HTTPError(f"Stream timeout after {timeout}s: {e}", status_code=408)
        except httpx.HTTPStatusError as e:
            raise self._transform_http_error(e)
        except httpx.RequestError as e:
            logger.error(f"Streaming request failed: {e}")
            raise HTTPError(f"Streaming request failed: {e}", status_code=0)
        except json_lib.JSONDecodeError as e:
            logger.error(f"Invalid streaming response format: {e}")
            raise HTTPError(f"Invalid streaming response format: {e}", status_code=502)

    async def close(self) -> None:
        """Close HTTP client and release resources."""
        if self._client:
            await self._client.aclose()
            self._client = None
