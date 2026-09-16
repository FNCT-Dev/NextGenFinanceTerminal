
import json

import pytest

from terminal.core.app_state import AppState
from terminal.core.config import Settings
from terminal.core.models import AssetClass, Candle, Quote
from terminal.onboarding.state import OnboardingState
from terminal.providers.synthetic import SyntheticMarketProvider


@pytest.mark.asyncio
async def test_synthetic_quote_contract() -> None:
    quote = await SyntheticMarketProvider().quote("NASDAQ:AAPL")

    assert isinstance(quote, Quote)
    assert quote.symbol == "NASDAQ:AAPL"
    assert quote.provider == "synthetic"
    assert quote.asset_class is AssetClass.EQUITY
    assert quote.freshness.value == "historical"


@pytest.mark.asyncio
async def test_synthetic_candle_contract_and_limit() -> None:
    candles = await SyntheticMarketProvider().candles("NASDAQ:AAPL", "1m", 4)

    assert len(candles) == 4
    assert all(isinstance(candle, Candle) for candle in candles)
    assert all(candle.provider == "synthetic" for candle in candles)
    assert all(candle.high >= candle.low for candle in candles)


def test_settings_load_defaults_without_optional_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key in ("NEXTGEN_ALPACA_API_KEY", "NEXTGEN_ALPACA_API_SECRET", "NEXTGEN_TIINGO_API_KEY"):
        monkeypatch.delenv(key, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "NextGen Finance Terminal"
    assert settings.alpaca_api_key is None
    assert settings.alpaca_api_secret is None
    assert settings.tiingo_api_key is None


def test_settings_loads_optional_environment_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEXTGEN_ALPACA_API_KEY", "synthetic-key")
    monkeypatch.setenv("NEXTGEN_ALPACA_API_SECRET", "synthetic-secret")

    settings = Settings(_env_file=None)

    assert settings.alpaca_api_key == "synthetic-key"
    assert settings.alpaca_api_secret == "synthetic-secret"


def test_app_state_serialization_preserves_set() -> None:
    state = AppState(
        onboarding_completed=True,
        pin_configured=True,
        enabled_providers={"synthetic", "ecos"},
    )

    payload = state.to_dict()
    restored = AppState.from_dict(json.loads(json.dumps(payload)))

    assert restored == state
    assert payload["enabled_providers"] == ["ecos", "synthetic"]


def test_onboarding_state_serialization_and_version_gate() -> None:
    state = OnboardingState(
        onboarding_completed=True,
        onboarding_version=2,
        pin_configured=True,
        current_step="finish",
    )

    restored = OnboardingState.model_validate(state.model_dump())

    assert restored == state
    assert not restored.requires_onboarding(2)
    assert restored.requires_onboarding(3)
