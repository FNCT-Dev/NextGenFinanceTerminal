from terminal.core.instruments import InstrumentRegistry


def test_korean_ticker_keeps_leading_zero() -> None:
    instrument = InstrumentRegistry.defaults().resolve("KRX:005930")
    assert instrument.provider_symbol == "005930"
