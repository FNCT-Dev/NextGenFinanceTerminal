from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from terminal.core.freshness import DataFreshness
from terminal.core.models import AssetClass, Quote


def test_delayed_label() -> None:
    assert DataFreshness.DELAYED.label(900) == "DELAYED 15M"


def test_quote_rejects_negative_delay() -> None:
    with pytest.raises(ValidationError):
        Quote(
            symbol="NASDAQ:AAPL",
            display_name="Apple",
            exchange="NASDAQ",
            asset_class=AssetClass.EQUITY,
            price=1,
            currency="USD",
            timestamp=datetime.now(UTC),
            provider="synthetic",
            freshness=DataFreshness.DELAYED,
            delay_seconds=-1,
        )
