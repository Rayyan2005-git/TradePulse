"""Backward-compatible shim for legacy imports."""

from config.registry import load_instruments
from infrastructure.providers.yfinance_provider import YFinanceProvider


def fetch_data(ticker_symbol, period="1mo", interval="1d"):
    """
    Legacy API: returns dict with history, current_price, previous_close, info.
    Prefer services.market_data.MarketDataService for new code.
    """
    instruments = load_instruments()
    instrument = next((i for i in instruments if i.symbol == ticker_symbol), None)
    if instrument is None:
        from domain.models import Instrument

        instrument = Instrument(
            id=ticker_symbol,
            name=ticker_symbol,
            symbol=ticker_symbol,
            category="unknown",
            currency="USD",
            price_format="${:,.2f}",
        )

    provider = YFinanceProvider()
    try:
        history = provider.get_history(instrument, period, interval)
        quote = provider.get_quote(instrument, period, interval)
        if quote.error:
            return None
        return {
            "history": history,
            "current_price": quote.price,
            "previous_close": quote.previous_close,
            "info": {},
        }
    except Exception:
        return None
