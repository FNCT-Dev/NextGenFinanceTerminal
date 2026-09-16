import pytest

from terminal.core.exceptions import AuthenticationError, RetryableProviderError
from terminal.core.provider_chain import ProviderChain


@pytest.mark.asyncio
async def test_falls_back_after_temporary_failure() -> None:
    async def unavailable() -> str:
        raise RetryableProviderError("temporary")

    async def secondary() -> str:
        return "Tiingo"

    assert await ProviderChain([unavailable, secondary]).execute() == "Tiingo"


@pytest.mark.asyncio
async def test_does_not_hide_authentication_error() -> None:
    async def invalid_key() -> str:
        raise AuthenticationError("invalid credential")

    with pytest.raises(AuthenticationError):
        await ProviderChain([invalid_key]).execute()
