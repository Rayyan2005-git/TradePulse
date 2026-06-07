import streamlit as st

from domain.analytics import format_change, format_price
from domain.models import Quote


def render_metric_card(quote: Quote) -> None:
    if not quote.is_valid:
        st.error(f"Failed to load {quote.name}")
        if quote.error:
            st.caption(quote.error)
        return

    symbol, delta_abs, delta_pct, css = format_change(quote)
    bg_css = "positive-bg" if css == "positive" else "negative-bg"
    
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-label">{quote.name}</span>
            </div>
            <div class="metric-value">{format_price(quote)}</div>
            <div class="metric-delta {css} {bg_css}">
                <span>{symbol}</span>
                <span>{delta_abs} ({delta_pct})</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_row(quotes: list[Quote], columns: int | None = None) -> None:
    n = columns or len(quotes)
    cols = st.columns(n)
    for col, quote in zip(cols, quotes):
        with col:
            render_metric_card(quote)
