from typing import Protocol

import pandas as pd

from domain.models import Instrument, Quote


class MarketDataProvider(Protocol):
    def get_history(
        self,
        instrument: Instrument,
        period: str,
        interval: str,
    ) -> pd.DataFrame:
        ...

    def get_quote(
        self,
        instrument: Instrument,
        period: str,
        interval: str,
    ) -> Quote:
        ...
