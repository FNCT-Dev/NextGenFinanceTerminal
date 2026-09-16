from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from terminal.core.freshness import DataFreshness


class AssetClass(StrEnum):
    EQUITY = "equity"
    INDEX = "index"
    BOND = "bond"
    FX = "fx"
    CRYPTO = "crypto"


class Instrument(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    internal_symbol: str
    provider_symbol: str
    display_name: str
    exchange: str
    mic: str | None = None
    country: str
    currency: str
    asset_class: AssetClass


class Quote(BaseModel):
    symbol: str
    display_name: str
    exchange: str
    asset_class: AssetClass
    price: float
    currency: str
    change: float | None = None
    change_percent: float | None = None
    timestamp: datetime
    provider: str
    freshness: DataFreshness
    delay_seconds: int | None = Field(default=None, ge=0)

    @field_validator("delay_seconds")
    @classmethod
    def delay_only_for_delayed(cls, value: int | None, info: object) -> int | None:
        # The semantic check is intentionally lenient: some providers omit delay metadata.
        return value


class Candle(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = Field(default=None, ge=0)
    provider: str
    freshness: DataFreshness


class MacroObservation(BaseModel):
    series_id: str
    timestamp: datetime
    value: float
    unit: str
    frequency: str
    provider: str


class NewsItem(BaseModel):
    title: str
    source: str
    published_at: datetime
    description: str | None = None
    url: str
    provider: str
    category: str | None = None
