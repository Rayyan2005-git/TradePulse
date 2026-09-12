"""Reusable metric card component styled for trading terminal."""

import streamlit as st

from domain.analytics import format_change, format_price
from domain.models import Quote


def render_metric_card(quote: Quote) -> None:
    """Render a single responsive trading card for an instrument quote."""
    if not quote.is_valid:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-label">{quote.name}</span>
                    <span class="metric-symbol-badge">{quote.symbol}</span>
                </div>
                <div class="metric-value" style="font-size: 18px; color: #EF5350;">Unavailable</div>
                <div class="freshness-bar" style="padding: 0;">{quote.error or 'Failed to fetch quote'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    symbol, delta_abs, delta_pct, css = format_change(quote)
    bg_css = "positive-bg" if css == "positive" else "negative-bg"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-label">{quote.name}</span>
                <span class="metric-symbol-badge">{quote.symbol}</span>
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


def render_metric_row(
    quotes: list[Quote],
    columns: int | None = None,
    max_cols: int = 4,
) -> None:
    """
    Render quotes in a responsive grid. If quotes count > max_cols and columns
    is not specified, chunks quotes into multiple rows of at most max_cols.
    """
    if not quotes:
        return

    if columns:
        cols = st.columns(columns)
        for col, quote in zip(cols, quotes):
            with col:
                render_metric_card(quote)
        return

    # Chunk into multiple rows for responsive, non-squeezed card layouts
    for i in range(0, len(quotes), max_cols):
        chunk = quotes[i : i + max_cols]
        cols = st.columns(len(chunk))
        for col, quote in zip(cols, chunk):
            with col:
                render_metric_card(quote)


def render_metric_skeletons(count: int = 4, columns: int = 4) -> None:
    """Render skeleton placeholder shimmer cards during load."""
    cols = st.columns(columns)
    for col in cols[:count]:
        with col:
            st.markdown('<div class="skeleton-card"></div>', unsafe_allow_html=True)
