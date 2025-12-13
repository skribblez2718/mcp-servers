"""Tests for rate limiter implementation.

Tests token bucket algorithm, concurrent requests, and token refill.
"""

import pytest
import asyncio
import time
from src.utils.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test rate limiter token bucket implementation."""

    @pytest.mark.asyncio
    async def test_rate_limiter_initialization(self):
        """Test rate limiter initializes correctly."""
        limiter = RateLimiter(rate=10.0, burst=20)

        assert limiter.rate == 10.0
        assert limiter.burst == 20
        assert limiter.tokens == 20.0  # Starts with full burst

    @pytest.mark.asyncio
    async def test_rate_limiter_default_burst(self):
        """Test rate limiter uses rate as default burst."""
        limiter = RateLimiter(rate=5.0)

        assert limiter.burst == 5
        assert limiter.tokens == 5.0

    @pytest.mark.asyncio
    async def test_acquire_single_token(self):
        """Test acquiring single token."""
        limiter = RateLimiter(rate=10.0, burst=10)

        await limiter.acquire()

        assert limiter.tokens == 9.0

    @pytest.mark.asyncio
    async def test_acquire_multiple_tokens(self):
        """Test acquiring multiple tokens sequentially."""
        limiter = RateLimiter(rate=10.0, burst=10)

        await limiter.acquire()
        await limiter.acquire()
        await limiter.acquire()

        assert limiter.tokens == 7.0

    @pytest.mark.asyncio
    async def test_acquire_waits_when_depleted(self):
        """Test acquire waits when tokens depleted."""
        limiter = RateLimiter(rate=10.0, burst=2)

        # Consume all tokens
        await limiter.acquire()
        await limiter.acquire()
        assert limiter.tokens == 0.0

        # Next acquire should wait
        start = time.monotonic()
        await limiter.acquire()
        elapsed = time.monotonic() - start

        # Should wait ~0.1s (1 token / 10 tokens per second)
        assert elapsed >= 0.09, "Should wait for token refill"

    @pytest.mark.asyncio
    async def test_try_acquire_success(self):
        """Test try_acquire returns True when token available."""
        limiter = RateLimiter(rate=10.0, burst=10)

        result = await limiter.try_acquire()

        assert result is True
        assert limiter.tokens == 9.0

    @pytest.mark.asyncio
    async def test_try_acquire_failure(self):
        """Test try_acquire returns False when no tokens."""
        limiter = RateLimiter(rate=10.0, burst=1)

        # Consume the token
        result1 = await limiter.try_acquire()
        assert result1 is True

        # No tokens left
        result2 = await limiter.try_acquire()
        assert result2 is False
        assert limiter.tokens == 0.0

    @pytest.mark.asyncio
    async def test_token_refill_over_time(self):
        """Test tokens refill based on elapsed time."""
        limiter = RateLimiter(rate=10.0, burst=10)

        # Consume all tokens
        for _ in range(10):
            await limiter.acquire()

        assert limiter.tokens == 0.0

        # Wait for refill (0.2s = 2 tokens at 10/s)
        await asyncio.sleep(0.2)

        # Should be able to acquire 2 more
        result1 = await limiter.try_acquire()
        result2 = await limiter.try_acquire()

        assert result1 is True
        assert result2 is True

    @pytest.mark.asyncio
    async def test_burst_cap_enforced(self):
        """Test tokens don't exceed burst limit."""
        limiter = RateLimiter(rate=10.0, burst=5)

        # Start with full burst
        assert limiter.tokens == 5.0

        # Wait longer than needed to refill (would give 10 tokens)
        await asyncio.sleep(1.0)

        # Try acquire should still work (tokens capped at burst)
        result = await limiter.try_acquire()
        assert result is True

        # Tokens shouldn't exceed burst
        assert limiter.tokens <= 5.0

    @pytest.mark.asyncio
    async def test_concurrent_acquires(self):
        """Test concurrent acquire calls are serialized."""
        limiter = RateLimiter(rate=100.0, burst=5)

        # Launch concurrent acquires
        tasks = [limiter.acquire() for _ in range(5)]
        await asyncio.gather(*tasks)

        # All tokens consumed
        assert limiter.tokens == 0.0

    @pytest.mark.asyncio
    async def test_high_rate_limit(self):
        """Test high rate limit (100 req/s)."""
        limiter = RateLimiter(rate=100.0, burst=100)

        # Should handle rapid acquires
        start = time.monotonic()
        for _ in range(50):
            await limiter.acquire()
        elapsed = time.monotonic() - start

        # Should be fast (no waiting needed with high burst)
        assert elapsed < 0.1

    @pytest.mark.asyncio
    async def test_low_rate_limit(self):
        """Test low rate limit (1 req/s)."""
        limiter = RateLimiter(rate=1.0, burst=2)

        # Consume burst
        await limiter.acquire()
        await limiter.acquire()

        # Next acquire waits 1 second
        start = time.monotonic()
        await limiter.acquire()
        elapsed = time.monotonic() - start

        assert elapsed >= 0.9, "Should wait ~1s at 1 req/s"

    @pytest.mark.asyncio
    async def test_fractional_rate(self):
        """Test fractional rate limit (0.5 req/s = 1 req per 2s)."""
        limiter = RateLimiter(rate=0.5, burst=1)

        await limiter.acquire()

        # Wait 2 seconds for next token
        await asyncio.sleep(2.0)

        result = await limiter.try_acquire()
        assert result is True
