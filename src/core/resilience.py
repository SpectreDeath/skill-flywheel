"""Resilience patterns for external API calls.

Provides circuit breaker, retry with backoff, and timeout decorators
with support for both sync and async functions.
"""

from __future__ import annotations

import asyncio
import functools
import threading
import time
from dataclasses import dataclass, field
from typing import Any, TypeVar
from collections.abc import Callable

try:
    import pybreaker

    PYBREAKER_AVAILABLE = True
except ImportError:
    PYBREAKER_AVAILABLE = False

T = TypeVar("T")


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker.

    Attributes:
        fail_max: Maximum number of failures before opening circuit.
        reset_timeout: Seconds to wait before attempting to close circuit.
        exclude: Tuple of exception types to not count as failures.
    """

    fail_max: int = 5
    reset_timeout: int = 60
    exclude: tuple = field(default_factory=tuple)


class ResilienceError(Exception):
    """Base exception for resilience-related errors."""

    pass


class CircuitOpenError(ResilienceError):
    """Circuit breaker is open."""

    pass


class RetryExhaustedError(ResilienceError):
    """Retries exhausted."""

    pass


class TimeoutError(ResilienceError):
    """Operation timed out."""

    pass


_circuit_breakers: dict[str, pybreaker.CircuitBreaker] = {}
_breakers_lock = threading.Lock()


def get_circuit_breaker(
    name: str = "default",
    config: CircuitBreakerConfig | None = None,
) -> pybreaker.CircuitBreaker:
    """Get or create a circuit breaker with the given config.

    Args:
        name: Name identifier for the circuit breaker.
        config: Configuration for the circuit breaker.

    Returns:
        A CircuitBreaker instance.
    """
    global _circuit_breakers

    with _breakers_lock:
        if name not in _circuit_breakers:
            if config is None:
                config = CircuitBreakerConfig()

            if PYBREAKER_AVAILABLE:
                breaker = pybreaker.CircuitBreaker(
                    fail_max=config.fail_max,
                    reset_timeout=config.reset_timeout,
                    exclude=config.exclude,
                )
            else:
                breaker = _SimpleCircuitBreaker(
                    fail_max=config.fail_max,
                    reset_timeout=config.reset_timeout,
                    exclude=config.exclude,
                )
            _circuit_breakers[name] = breaker

        return _circuit_breakers[name]


def circuit_breaker(
    name: str = "default",
    config: CircuitBreakerConfig | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for wrapping functions with circuit breaker.

    Args:
        name: Name identifier for the circuit breaker.
        config: Configuration for the circuit breaker.

    Returns:
        Decorated function with circuit breaker protection.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        breaker = get_circuit_breaker(name, config)

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                try:
                    return await breaker.call(func, *args, **kwargs)
                except pybreaker.CircuitError as e:
                    raise CircuitOpenError(f"Circuit open: {e}") from e
                except Exception as e:
                    if PYBREAKER_AVAILABLE and isinstance(e, pybreaker.CircuitError):
                        raise CircuitOpenError(f"Circuit open: {e}") from e
                    raise

            return async_wrapper  # type: ignore[return-value]
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> T:
                try:
                    return breaker.call(func, *args, **kwargs)
                except pybreaker.CircuitError as e:
                    raise CircuitOpenError(f"Circuit open: {e}") from e
                except Exception as e:
                    if PYBREAKER_AVAILABLE and isinstance(e, pybreaker.CircuitError):
                        raise CircuitOpenError(f"Circuit open: {e}") from e
                    raise

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retry with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds.
        max_delay: Maximum delay between retries.
        exponential_base: Base for exponential backoff.
        exceptions: Tuple of exception types to retry on.

    Returns:
        Decorated function with retry logic.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Exception | None = None

                for attempt in range(max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt < max_retries:
                            delay = min(
                                base_delay * (exponential_base**attempt),
                                max_delay,
                            )
                            await asyncio.sleep(delay)
                        else:
                            raise RetryExhaustedError(
                                f"Retries exhausted after {max_retries} attempts"
                            ) from last_exception

                raise RetryExhaustedError(
                    f"Retries exhausted after {max_retries} attempts"
                ) from last_exception

            return async_wrapper  # type: ignore[return-value]
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Exception | None = None

                for attempt in range(max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt < max_retries:
                            delay = min(
                                base_delay * (exponential_base**attempt),
                                max_delay,
                            )
                            time.sleep(delay)
                        else:
                            raise RetryExhaustedError(
                                f"Retries exhausted after {max_retries} attempts"
                            ) from last_exception

                raise RetryExhaustedError(
                    f"Retries exhausted after {max_retries} attempts"
                ) from last_exception

            return sync_wrapper  # type: ignore[return-value]

    return decorator


def timeout(seconds: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for adding timeout to async functions.

    Args:
        seconds: Timeout in seconds.

    Returns:
        Decorated function with timeout protection.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                try:
                    return await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=seconds,
                    )
                except asyncio.TimeoutError as e:
                    raise TimeoutError(
                        f"Operation timed out after {seconds} seconds"
                    ) from e

            return async_wrapper  # type: ignore[return-value]
        else:
            raise TypeError("timeout decorator is only supported for async functions")

    return decorator


class _SimpleCircuitBreaker:
    """Simple in-memory circuit breaker implementation.

    Used when pybreaker is not available.
    """

    def __init__(
        self,
        fail_max: int = 5,
        reset_timeout: int = 60,
        exclude: tuple = (),
    ) -> None:
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.exclude = exclude
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._state = "closed"
        self._lock = threading.Lock()

    @property
    def state(self) -> str:
        with self._lock:
            if self._state == "open":
                if self._last_failure_time is not None:
                    if time.time() - self._last_failure_time >= self.reset_timeout:
                        self._state = "half-open"
            return self._state

    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        with self._lock:
            if self.state == "open":
                raise CircuitOpenError("Circuit breaker is open")

            if self.state == "half-open":
                pass

        try:
            result = func(*args, **kwargs)
            with self._lock:
                self._failure_count = 0
                self._state = "closed"
            return result
        except Exception as e:
            if isinstance(e, self.exclude):
                raise

            with self._lock:
                self._failure_count += 1
                self._last_failure_time = time.time()

                if self._failure_count >= self.fail_max:
                    self._state = "open"

            raise
