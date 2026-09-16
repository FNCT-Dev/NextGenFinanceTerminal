from abc import ABC, abstractmethod
from datetime import datetime

from terminal.core.models import Candle, MacroObservation, NewsItem, Quote


class QuoteProvider(ABC):
    @abstractmethod
    async def quote(self, symbol: str) -> Quote: ...


class IntradayProvider(ABC):
    @abstractmethod
    async def candles(self, symbol: str, interval: str, limit: int) -> list[Candle]: ...


class HistoricalProvider(ABC):
    @abstractmethod
    async def candles(
        self, symbol: str, interval: str, start: datetime, end: datetime
    ) -> list[Candle]: ...


class FundamentalProvider(ABC):
    @abstractmethod
    async def fundamentals(self, symbol: str) -> dict[str, object]: ...


class MacroProvider(ABC):
    @abstractmethod
    async def series(
        self, series_id: str, start: datetime, end: datetime
    ) -> list[MacroObservation]: ...


class NewsProvider(ABC):
    @abstractmethod
    async def latest(self) -> list[NewsItem]: ...

    @abstractmethod
    async def search(self, query: str) -> list[NewsItem]: ...


class RealtimeProvider(ABC):
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def subscribe(self, symbol: str) -> None: ...

    @abstractmethod
    async def unsubscribe(self, symbol: str) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...
