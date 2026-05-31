from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class Instrument:
    id: str
    name: str
    symbol: str
    category: str
    currency: str
    price_format: str


@dataclass
class Quote:
    instrument_id: str
    symbol: str
    name: str
    price: float
    previous_close: float
    currency: str
    price_format: str
    as_of: Optional[datetime] = None
    error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.error is None and self.previous_close != 0


@dataclass
class InstrumentSeries:
    instrument_id: str
    symbol: str
    name: str
    history: pd.DataFrame = field(default_factory=pd.DataFrame)
    error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.error is None and not self.history.empty


@dataclass
class MarketSnapshot:
    quotes: dict[str, Quote]
    series: dict[str, InstrumentSeries]
    fetched_at: datetime
    source: str
    period: str
    interval: str
    load_errors: list[str] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for q in self.quotes.values() if q.is_valid)

    @property
    def total_count(self) -> int:
        return len(self.quotes)
