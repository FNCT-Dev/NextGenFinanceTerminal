# Architecture

Phase 1 dependency direction is UI → services → provider interfaces → provider adapters. `terminal.core` does not import UI or providers. Providers normalize outputs to `Quote`, `Candle`, `MacroObservation`, and `NewsItem`; raw payloads stay inside adapters.

`InstrumentRegistry` resolves canonical symbols such as `KRX:005930` and preserves leading zeroes. `ProviderChain` retries only temporary failures and then tries the next provider. Authentication, permission, invalid-symbol, and configuration failures deliberately bypass fallback. No database, event bus, plugin framework, or DI container is introduced.

