from domain.models import Quote


def change_abs(quote: Quote) -> float:
    return quote.price - quote.previous_close


def change_pct(quote: Quote) -> float:
    if quote.previous_close == 0:
        return 0.0
    return (change_abs(quote) / quote.previous_close) * 100


def format_price(quote: Quote) -> str:
    return quote.price_format.format(quote.price)


def format_change(quote: Quote) -> tuple[str, str, str, str]:
    """Returns (delta_symbol, abs_change_str, pct_str, css_class)."""
    delta = change_abs(quote)
    pct = change_pct(quote)
    symbol = "▲" if delta >= 0 else "▼"
    css = "positive" if delta >= 0 else "negative"
    return symbol, f"{abs(delta):,.2f}", f"{abs(pct):.2f}%", css


def normalized_returns(history_close_series) -> "pd.Series":
    """Daily % returns from close prices."""
    import pandas as pd

    closes = history_close_series.dropna()
    if closes.empty:
        return pd.Series(dtype=float)
    return closes.pct_change().dropna()


def calculate_sma(series: "pd.Series", window: int = 20) -> "pd.Series":
    """Calculate Simple Moving Average."""
    return series.rolling(window=window).mean()


def calculate_rsi(series: "pd.Series", window: int = 14) -> "pd.Series":
    """Calculate Relative Strength Index."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
