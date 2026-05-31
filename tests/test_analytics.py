from domain.analytics import change_abs, change_pct, format_price
from domain.models import Quote


def _quote(price: float, prev: float) -> Quote:
    return Quote(
        instrument_id="test",
        symbol="TEST",
        name="Test",
        price=price,
        previous_close=prev,
        currency="USD",
        price_format="${:,.2f}",
    )


def test_change_pct_positive():
    q = _quote(110.0, 100.0)
    assert change_abs(q) == 10.0
    assert change_pct(q) == 10.0


def test_change_pct_negative():
    q = _quote(90.0, 100.0)
    assert change_abs(q) == -10.0
    assert change_pct(q) == -10.0


def test_format_price_usd():
    q = _quote(2045.5, 2000.0)
    assert format_price(q) == "$2,045.50"


def test_format_price_inr():
    q = Quote(
        instrument_id="usd_inr",
        symbol="INR=X",
        name="USD/INR",
        price=83.25,
        previous_close=83.0,
        currency="INR",
        price_format="₹{:,.2f}",
    )
    assert format_price(q) == "₹83.25"
