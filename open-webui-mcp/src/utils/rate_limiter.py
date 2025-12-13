"""Token bucket rate limiter implementation.

Provides client-side rate limiting to prevent overwhelming the API.
"""

import asyncio
import time
from typing import Optional


class RateLimiter:
    """Token bucket rate limiter.

    Args:
        rate: Requests per second allowed
        burst: Maximum burst size (defaults to rate)
    """

    def __init__(self, rate: float, burst: Optional[int] = None) -> None:
        """Initialize rate limiter.

        Args:
            rate: Requests per second
            burst: Optional burst size
        """
        self.rate = rate
        self.burst = burst or int(rate)
        self.tokens = float(self.burst)
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary.

        This method blocks until a token is available.
        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(
                self.burst,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Wait if no tokens available
            if self.tokens < 1.0:
                wait_time = (1.0 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)

                # Update after waiting
                now = time.monotonic()
                elapsed = now - self.last_update
                self.tokens = min(
                    self.burst,
                    self.tokens + elapsed * self.rate
                )
                self.last_update = now

            # Consume one token
            self.tokens -= 1.0

    async def try_acquire(self) -> bool:
        """Try to acquire a token without waiting.

        Returns:
            True if token acquired, False otherwise
        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(
                self.burst,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Check if token available
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True

            return False
