from datetime import datetime, timezone
from functools import lru_cache
from typing import Optional

import certifi
import pandas as pd
import yfinance as yf
from curl_cffi import requests as curl_requests

from domain.models import Instrument, Quote
from infrastructure.providers.base import MarketDataProvider


@lru_cache(maxsize=1)
def _yahoo_session() -> curl_requests.Session:
    """Use certifi bundle; fall back to verify=False if local SSL trust is broken."""
    verify = certifi.where()
    session = curl_requests.Session(impersonate="chrome")
    session.verify = verify
    try:
        probe = yf.Ticker("GC=F", session=session)
        hist = probe.history(period="5d")
        if hist is None or hist.empty:
            raise ValueError("empty probe")
    except Exception:
        session = curl_requests.Session(impersonate="chrome")
        session.verify = False
    return session


class YFinanceProvider:
    """Fetches market data from Yahoo Finance via yfinance."""

    def get_history(
        self,
        instrument: Instrument,
        period: str = "1mo",
        interval: str = "1d",
    ) -> pd.DataFrame:
        ticker = yf.Ticker(instrument.symbol, session=_yahoo_session())
        history = ticker.history(period=period, interval=interval)
        if history is None or history.empty:
            raise ValueError(f"No history returned for {instrument.symbol}")
        return history

    def get_quote(
        self,
        instrument: Instrument,
        period: str = "1mo",
        interval: str = "1d",
    ) -> Quote:
        try:
            history = self.get_history(instrument, period, interval)
            price = float(history["Close"].iloc[-1])

            if len(history) > 1:
                previous_close = float(history["Close"].iloc[-2])
            else:
                previous_close = price

            as_of = _extract_as_of(history)
            return Quote(
                instrument_id=instrument.id,
                symbol=instrument.symbol,
                name=instrument.name,
                price=price,
                previous_close=previous_close,
                currency=instrument.currency,
                price_format=instrument.price_format,
                as_of=as_of,
            )
        except Exception as exc:
            return Quote(
                instrument_id=instrument.id,
                symbol=instrument.symbol,
                name=instrument.name,
                price=0.0,
                previous_close=0.0,
                currency=instrument.currency,
                price_format=instrument.price_format,
                error=str(exc),
            )


def _extract_as_of(history: pd.DataFrame) -> Optional[datetime]:
    if history.empty:
        return None
    ts = history.index[-1]
    if hasattr(ts, "to_pydatetime"):
        dt = ts.to_pydatetime()
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    return datetime.now(timezone.utc)
