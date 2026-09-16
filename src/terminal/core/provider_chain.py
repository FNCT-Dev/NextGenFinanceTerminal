from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from terminal.core.exceptions import RetryableProviderError

T = TypeVar("T")


class ProviderChain(Generic[T]):
    """Retries temporary errors per provider, then tries the next provider."""

    def __init__(self, providers: list[Callable[[], Awaitable[T]]]) -> None:
        self._providers = providers

    async def execute(self) -> T:
        last_error: RetryableProviderError | None = None
        for provider in self._providers:
            try:
                return await self._retry(provider)
            except RetryableProviderError as error:
                last_error = error
        if last_error is not None:
            raise last_error
        raise RuntimeError("Provider chain has no providers")

    @retry(
        retry=retry_if_exception_type(RetryableProviderError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.1, max=1),
        reraise=True,
    )
    async def _retry(self, provider: Callable[[], Awaitable[T]]) -> T:
        return await provider()
