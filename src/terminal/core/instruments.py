import re

from terminal.core.exceptions import InvalidSymbolError, UnknownSymbolError
from terminal.core.models import AssetClass, Instrument

_CANONICAL_SYMBOL = re.compile(r"^[A-Z][A-Z0-9_-]*:[^:\s]+$")

class InstrumentRegistry:
    """Canonical-symbol registry. Provider adapters own non-canonical conversion."""

    def __init__(self, instruments: list[Instrument] | None = None) -> None:
        self._items = {item.internal_symbol: item for item in instruments or []}

    def register(self, instrument: Instrument) -> None:
        self._items[instrument.internal_symbol] = instrument

    def resolve(self, canonical_symbol: str) -> Instrument:
        if not isinstance(canonical_symbol, str) or not _CANONICAL_SYMBOL.fullmatch(
        canonical_symbol
        ):
            raise InvalidSymbolError(f"Invalid canonical symbol: {canonical_symbol!r}")

        try:
            return self._items[canonical_symbol]
        except KeyError as error:
             raise UnknownSymbolError(
                f"Unknown canonical symbol: {canonical_symbol}"
            ) from error

    @classmethod
    def defaults(cls) -> "InstrumentRegistry":
        return cls(
            [
                Instrument(
                    internal_symbol="KRX:005930",
                    provider_symbol="005930",
                    display_name="Samsung Electronics",
                    exchange="KRX",
                    mic="XKRX",
                    country="KR",
                    currency="KRW",
                    asset_class=AssetClass.EQUITY,
                ),
                Instrument(
                    internal_symbol="NASDAQ:AAPL",
                    provider_symbol="AAPL",
                    display_name="Apple Inc.",
                    exchange="NASDAQ",
                    mic="XNAS",
                    country="US",
                    currency="USD",
                    asset_class=AssetClass.EQUITY,
                ),
            ]
        )
