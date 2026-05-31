from typing import List

import pandas as pd

from config.registry import filter_by_category, load_instruments
from domain.analytics import change_abs, change_pct
from domain.models import Instrument, MarketSnapshot, Quote


class DashboardService:
    @staticmethod
    def instruments_for_page(category: str | None = None) -> List[Instrument]:
        instruments = load_instruments()
        if category:
            return filter_by_category(instruments, category)
        return instruments

    @staticmethod
    def instrument_ids(instruments: List[Instrument]) -> tuple[str, ...]:
        return tuple(i.id for i in instruments)

    @staticmethod
    def ordered_quotes(
        snapshot: MarketSnapshot, instruments: List[Instrument]
    ) -> List[Quote]:
        return [
            snapshot.quotes[inst.id]
            for inst in instruments
            if inst.id in snapshot.quotes
        ]

    @staticmethod
    def comparison_dataframe(snapshot: MarketSnapshot) -> pd.DataFrame:
        """Normalized cumulative return comparison across instruments."""
        rows = {}
        for inst_id, inst_series in snapshot.series.items():
            if not inst_series.is_valid:
                continue
            closes = inst_series.history["Close"].dropna()
            if closes.empty:
                continue
            normalized = (closes / closes.iloc[0] - 1) * 100
            quote = snapshot.quotes.get(inst_id)
            label = quote.name if quote else inst_id
            rows[label] = normalized

        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)

    @staticmethod
    def spread_summary(snapshot: MarketSnapshot) -> pd.DataFrame:
        """Simple 1-day change summary for FX vs commodities."""
        data = []
        for quote in snapshot.quotes.values():
            if not quote.is_valid:
                continue
            data.append(
                {
                    "Instrument": quote.name,
                    "Price": quote.price_format.format(quote.price),
                    "Change": f"{change_abs(quote):+,.2f}",
                    "Change %": f"{change_pct(quote):+.2f}%",
                }
            )
        return pd.DataFrame(data)
