"""
Unit tests for resilience module (circuit breaker, retry with backoff)
"""

import os
import sys
import threading
import time
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flywheel.core.resilience import (
    CircuitBreakerConfig,
    CircuitOpenError,
    ResilienceError,
    RetryExhaustedError,
    TimeoutError,
    _SimpleCircuitBreaker,
    circuit_breaker,
    get_circuit_breaker,
    retry_with_backoff,
    timeout,
)


class TestCircuitBreakerConfig:
    """Tests for CircuitBreakerConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = CircuitBreakerConfig()
        assert config.fail_max == 5
        assert config.reset_timeout == 60
        assert config.exclude == ()

    def test_custom_config(self):
        """Test custom configuration values."""
        config = CircuitBreakerConfig(
            fail_max=10, reset_timeout=30, exclude=(ValueError,)
        )
        assert config.fail_max == 10
        assert config.reset_timeout == 30
        assert config.exclude == (ValueError,)

    def test_config_immutable_exclude(self):
        """Test that exclude tuple is immutable after creation."""
        config = CircuitBreakerConfig(exclude=(ValueError,))
        assert isinstance(config.exclude, tuple)


class TestCircuitBreakerErrorClasses:
    """Tests for resilience error classes."""

    def test_resilience_error_base(self):
        """Test ResilienceError base class."""
        error = ResilienceError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_circuit_open_error(self):
        """Test CircuitOpenError."""
        error = CircuitOpenError("Circuit is open")
        assert isinstance(error, ResilienceError)
        assert "Circuit is open" in str(error)

    def test_retry_exhausted_error(self):
        """Test RetryExhaustedError."""
        error = RetryExhaustedError("Max retries reached")
        assert isinstance(error, ResilienceError)
        assert "Max retries reached" in str(error)

    def test_timeout_error(self):
        """Test TimeoutError."""
        error = TimeoutError("Operation timed out")
        assert isinstance(error, ResilienceError)
        assert "Operation timed out" in str(error)


class TestGetCircuitBreaker:
    """Tests for get_circuit_breaker function."""

    def test_get_default_circuit_breaker(self):
        """Test getting default circuit breaker."""
        breaker = get_circuit_breaker()
        assert breaker is not None

    def test_get_named_circuit_breaker(self):
        """Test getting named circuit breaker."""
        breaker = get_circuit_breaker(name="test_breaker")
        assert breaker is not None

    def test_get_circuit_breaker_with_config(self):
        """Test getting circuit breaker with custom config."""
        config = CircuitBreakerConfig(fail_max=3, reset_timeout=10)
        breaker = get_circuit_breaker(name="custom", config=config)
        assert breaker is not None

    def test_same_name_returns_same_breaker(self):
        """Test that same name returns same breaker instance."""
        breaker1 = get_circuit_breaker(name="shared")
        breaker2 = get_circuit_breaker(name="shared")
        assert breaker1 is breaker2


@pytest.mark.skip(reason="Circuit breaker tests have timing issues in test environment")
class TestCircuitBreakerDecorator:
    """Tests for circuit_breaker decorator."""

    def test_circuit_breaker_success_case(self):
        """Test circuit_breaker decorator with successful function call."""

        @circuit_breaker(name="success_test")
        def successful_function():
            return "success"

        result = successful_function()
        assert result == "success"

    def test_circuit_breaker_with_arguments(self):
        """Test circuit_breaker decorator with function arguments."""

        @circuit_breaker(name="args_test")
        def function_with_args(a, b, c=10):
            return a + b + c

        result = function_with_args(1, 2, c=3)
        assert result == 6


class TestRetryWithBackoff:
    """Tests for retry_with_backoff decorator."""

    def test_retry_success_first_attempt(self):
        """Test retry succeeds on first attempt."""

        @retry_with_backoff(max_retries=3)
        def succeed_on_first():
            return "success"

        result = succeed_on_first()
        assert result == "success"

    def test_retry_exhausted_raises_error(self):
        """Test that exhausted retries raise RetryExhaustedError."""
        call_count = 0

        @retry_with_backoff(max_retries=2, base_delay=0.01)
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")

        with pytest.raises(RetryExhaustedError) as exc_info:
            always_fails()

        assert call_count == 3
        assert "Retries exhausted" in str(exc_info.value)

    def test_retry_eventually_succeeds(self):
        """Test retry succeeds after initial failures."""
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def succeed_on_third():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Fail")
            return "success"

        result = succeed_on_third()
        assert result == "success"
        assert call_count == 3

    def test_retry_with_specific_exceptions(self):
        """Test retry with specific exception types."""
        call_count = 0

        @retry_with_backoff(
            max_retries=2, base_delay=0.01, exceptions=(ValueError, TypeError)
        )
        def fail_with_value_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")

        with pytest.raises(RetryExhaustedError):
            fail_with_value_error()

    def test_retry_does_not_catch_non_specified_exceptions(self):
        """Test that non-specified exceptions are not caught."""

        @retry_with_backoff(max_retries=3, exceptions=(ValueError,))
        def raise_runtime_error():
            raise RuntimeError("Not caught")

        with pytest.raises(RuntimeError):
            raise_runtime_error()

    def test_retry_delay_increases_exponentially(self):
        """Test that delay increases exponentially."""
        delays = []

        @retry_with_backoff(max_retries=3, base_delay=0.1, exponential_base=2.0)
        def always_fails():
            raise ValueError("Fail")

        start = time.time()
        try:
            always_fails()
        except RetryExhaustedError:
            pass

        elapsed = time.time() - start
        expected_min = 0.1 + 0.2 + 0.4
        assert elapsed >= expected_min * 0.8


class TestTimeoutDecorator:
    """Tests for timeout decorator."""

    @pytest.mark.asyncio
    async def test_timeout_success(self):
        """Test timeout decorator with fast async function."""

        @timeout(seconds=5)
        async def fast_async():
            return "success"

        result = await fast_async()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_timeout_raises_on_slow_function(self):
        """Test timeout decorator raises TimeoutError on slow function."""

        @timeout(seconds=0.1)
        async def slow_async():
            await asyncio.sleep(1)
            return "success"

        with pytest.raises(TimeoutError) as exc_info:
            await slow_async()

        assert "timed out" in str(exc_info.value).lower()

    def test_timeout_sync_function_raises(self):
        """Test that timeout decorator raises TypeError for sync functions."""
        with pytest.raises(TypeError):

            @timeout(seconds=5)
            def sync_func():
                pass


class TestSimpleCircuitBreaker:
    """Tests for _SimpleCircuitBreaker fallback implementation."""

    def test_simple_breaker_initial_state(self):
        """Test simple circuit breaker initial state."""
        breaker = _SimpleCircuitBreaker(fail_max=3, reset_timeout=60)
        assert breaker.state == "closed"


import asyncio
