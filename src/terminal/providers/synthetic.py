from datetime import UTC, datetime, timedelta

from terminal.core.freshness import DataFreshness
from terminal.core.models import AssetClass, Candle, Quote
from terminal.providers.interfaces import IntradayProvider, QuoteProvider


class SyntheticMarketProvider(QuoteProvider, IntradayProvider):
    """Deterministic, non-market-data provider for development and tests."""

    name = "synthetic"

    async def quote(self, symbol: str) -> Quote:
        return Quote(
            symbol=symbol,
            display_name=f"Synthetic {symbol}",
            exchange="SYNTH",
            asset_class=AssetClass.EQUITY,
            price=100.0,
            currency="USD",
            change=1.25,
            change_percent=1.27,
            timestamp=datetime.now(UTC),
            provider=self.name,
            freshness=DataFreshness.HISTORICAL,
        )

    async def candles(self, symbol: str, interval: str, limit: int) -> list[Candle]:
        now = datetime.now(UTC).replace(second=0, microsecond=0)
        return [
            Candle(
                timestamp=now - timedelta(minutes=index),
                open=99.0,
                high=101.0,
                low=98.5,
                close=100.0,
                volume=1000.0 + index,
                provider=self.name,
                freshness=DataFreshness.HISTORICAL,
            )
            for index in range(limit)
        ]
