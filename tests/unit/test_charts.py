from datetime import UTC, datetime

import pytest

from terminal.core.freshness import DataFreshness
from terminal.core.models import Candle
from terminal.ui.charts import YieldCurveChart, candle_payload


def _candle(timestamp: datetime, close: float = 101.0) -> Candle:
    return Candle(
        timestamp=timestamp,
        open=100.0,
        high=102.0,
        low=99.0,
        close=close,
        volume=123.0,
        provider="synthetic",
        freshness=DataFreshness.HISTORICAL,
    )


def test_candle_payload_orders_normalized_models_by_timestamp() -> None:
    later = _candle(datetime(2026, 1, 1, 0, 1, tzinfo=UTC))
    earlier = _candle(datetime(2026, 1, 1, 0, 0, tzinfo=UTC))

    payload = candle_payload((later, earlier))

    assert [item["time"] for item in payload] == [1_767_225_600, 1_767_225_660]
    assert payload[0]["volume"] == 123.0
    assert set(payload[0]) == {"time", "open", "high", "low", "close", "volume"}


def test_delayed_freshness_labels_minutes_and_weeks() -> None:
    assert DataFreshness.DELAYED.label(900) == "DELAYED 15M"
    assert DataFreshness.DELAYED.label(1_209_600) == "DELAYED 2W"


def test_yield_curve_rejects_mismatched_points() -> None:
    with pytest.raises(ValueError, match="same length"):
        YieldCurveChart.set_curve(object(), (1.0,), (2.0, 3.0))  # type: ignore[arg-type]
