# Third-party data policy

The source-code license applies only to the original source code contained in this repository. Market data, economic statistics, news metadata, trademarks, and other third-party content accessed at runtime remain subject to the terms and licenses of their respective providers.

Phase 1 ships no live data adapter and makes no runtime market-data requests. Future provider integrations must be reviewed against official documentation before activation.

| Provider | Intended use | Credential | Default | Retention / redistribution |
| --- | --- | --- | --- | --- |
| SyntheticMarketProvider | Development and tests only | No | Enabled in development | Synthetic data only |
| Alpaca | US market data (future) | Yes | Disabled | Review current terms; no redistribution |
| Tiingo | US fallback (future) | Yes | Disabled | Review current terms; no redistribution |
| KRX / ECOS | Korean market and macro (future) | Varies | Disabled | Review official terms; no repository storage |
| J-Quants / JPX | Japan historical / delayed quote (future) | Varies | Disabled | Review official terms; no repository storage |

## Bundled chart dependency

| Component | Version | Use | License | Distribution |
| --- | --- | --- | --- | --- |
| TradingView Lightweight Charts | 5.0.9 | Local QtWebEngine candlestick and volume rendering | Apache-2.0 | Bundled standalone asset; no market data included |

Future adapters must record official docs, free/paid status, personal/commercial/external-display conditions, attribution, cache/persistence, and redistribution terms. Default policy: in-memory TTL cache only; no central data relay.
