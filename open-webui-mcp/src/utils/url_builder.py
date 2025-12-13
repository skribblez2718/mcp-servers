"""URL building utilities with safe parameter encoding."""

from urllib.parse import urlencode, quote
from typing import Any


def build_url(base_url: str, endpoint: str, params: dict[str, Any] | None = None) -> str:
    """Build URL with safe parameter encoding.

    Args:
        base_url: Base URL (without trailing slash)
        endpoint: Endpoint path (with leading slash)
        params: Query parameters

    Returns:
        Complete URL with encoded parameters
    """
    # Ensure base_url has no trailing slash
    base_url = base_url.rstrip("/")

    # Ensure endpoint has leading slash
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Build base URL
    url = base_url + endpoint

    # Add query parameters if present
    if params:
        # Filter out None values
        filtered_params = {k: v for k, v in params.items() if v is not None}

        if filtered_params:
            # Encode parameters
            query_string = urlencode(filtered_params, safe="", quote_via=quote)
            url = f"{url}?{query_string}"

    return url


def encode_path_component(component: str) -> str:
    """Encode a path component safely.

    Args:
        component: Path component to encode

    Returns:
        URL-encoded component
    """
    return quote(component, safe="")
