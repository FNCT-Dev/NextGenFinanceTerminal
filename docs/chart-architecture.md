# Chart architecture

## Phase 3 implementation

`terminal.ui.charts.CandlestickChart` is a QtWebEngine host with a deliberately
small browser contract: `setData(candles)` and `update(candle)`. It receives
only normalized `Candle` models, converted to OHLCV dictionaries by
`candle_payload`; it never imports a provider or accepts raw API responses.

The embedded HTML owns rendering and is disposed explicitly when its Qt widget
closes. It loads the vendored TradingView Lightweight Charts v5 standalone
bundle locally, so chart creation does not depend on network access. The public
browser contract exposes `setData` and `update` while keeping the renderer
replaceable without changing core models or UI callers.

`YieldCurveChart` uses PyQtGraph and accepts ordered maturities and normalized
yield values. It is reserved for Phase 8 provider data.

Freshness remains data-owned: badges render `LIVE`, `DELAYED`, `EOD`, or
`HISTORICAL` from the normalized model and never infer real-time status.
