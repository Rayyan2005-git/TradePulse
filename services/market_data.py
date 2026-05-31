from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import List, Optional

import streamlit as st

from config.registry import load_instruments
from config.settings import DATA_SOURCE_LABEL, DEFAULT_INTERVAL, DEFAULT_PERIOD
from domain.models import Instrument, InstrumentSeries, MarketSnapshot, Quote
from infrastructure.providers.yfinance_provider import YFinanceProvider


class MarketDataService:
    def __init__(self, provider: Optional[YFinanceProvider] = None):
        self._provider = provider or YFinanceProvider()

    def get_snapshot(
        self,
        instruments: Optional[List[Instrument]] = None,
        period: str = DEFAULT_PERIOD,
        interval: str = DEFAULT_INTERVAL,
    ) -> MarketSnapshot:
        items = instruments or load_instruments()
        quotes: dict[str, Quote] = {}
        series: dict[str, InstrumentSeries] = {}
        errors: list[str] = []

        with ThreadPoolExecutor(max_workers=min(4, len(items) or 1)) as executor:
            quote_futures = {
                executor.submit(
                    _cached_quote, inst.id, inst.symbol, inst.name,
                    inst.currency, inst.price_format, period, interval,
                ): inst
                for inst in items
            }
            series_futures = {
                executor.submit(
                    _cached_series, inst.id, inst.symbol, inst.name, period, interval,
                ): inst
                for inst in items
            }

            for future in as_completed(quote_futures):
                inst = quote_futures[future]
                quote = future.result()
                quotes[inst.id] = quote
                if quote.error:
                    errors.append(f"{inst.name} ({inst.symbol}): {quote.error}")

            for future in as_completed(series_futures):
                inst = series_futures[future]
                inst_series = future.result()
                series[inst.id] = inst_series
                if inst_series.error:
                    errors.append(f"{inst.name} chart: {inst_series.error}")

        return MarketSnapshot(
            quotes=quotes,
            series=series,
            fetched_at=datetime.now(timezone.utc),
            source=DATA_SOURCE_LABEL,
            period=period,
            interval=interval,
            load_errors=errors,
        )


@st.cache_data(ttl=120, show_spinner=False)
def _cached_quote(
    instrument_id: str,
    symbol: str,
    name: str,
    currency: str,
    price_format: str,
    period: str,
    interval: str,
) -> Quote:
    instrument = Instrument(
        id=instrument_id,
        name=name,
        symbol=symbol,
        category="",
        currency=currency,
        price_format=price_format,
    )
    return YFinanceProvider().get_quote(instrument, period, interval)


@st.cache_data(ttl=600, show_spinner=False)
def _cached_series(
    instrument_id: str,
    symbol: str,
    name: str,
    period: str,
    interval: str,
) -> InstrumentSeries:
    instrument = Instrument(
        id=instrument_id,
        name=name,
        symbol=symbol,
        category="",
        currency="",
        price_format="",
    )
    provider = YFinanceProvider()
    try:
        history = provider.get_history(instrument, period, interval)
        return InstrumentSeries(
            instrument_id=instrument_id,
            symbol=symbol,
            name=name,
            history=history,
        )
    except Exception as exc:
        return InstrumentSeries(
            instrument_id=instrument_id,
            symbol=symbol,
            name=name,
            error=str(exc),
        )


def get_cached_snapshot(
    instrument_ids: tuple[str, ...],
    period: str,
    interval: str,
) -> MarketSnapshot:
    """Build a snapshot from per-instrument cached fetches."""
    all_instruments = load_instruments()
    selected = [i for i in all_instruments if i.id in instrument_ids]
    if not selected:
        selected = all_instruments
    return MarketDataService().get_snapshot(selected, period, interval)
