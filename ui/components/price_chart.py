"""Plotly price charting components styled for the trading terminal theme."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from domain.analytics import calculate_sma
from domain.models import InstrumentSeries

# Trading terminal theme constants
CHART_BG = "#0B0E14"
PANEL_BG = "#131722"
COLOR_TEAL = "#26A69A"
COLOR_RED = "#EF5350"
COLOR_AMBER = "#E8A33D"
COLOR_TEXT_PRIMARY = "#E8E8E8"
COLOR_TEXT_MUTED = "#8A8D93"
COLOR_GRID = "rgba(255, 255, 255, 0.06)"
COLOR_ZERO = "rgba(255, 255, 255, 0.15)"


def render_candlestick(series: InstrumentSeries, height: int = 580, key: str | None = None) -> None:
    """Render a terminal-styled Candlestick chart with SMA-20 overlay and volume bars."""
    if not series.is_valid:
        st.info("No historical data available to display chart.")
        if series.error:
            st.caption(series.error)
        return

    hist = series.history

    # Subplots: 2 rows (Price 75%, Volume 25%)
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        subplot_titles=(f"{series.name} — Price Movement", "Volume"),
        row_heights=[0.75, 0.25],
    )

    # 1. Candlestick Trace with terminal teal/red palette
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            name="Candlestick",
            increasing=dict(
                line=dict(color=COLOR_TEAL, width=1.2),
                fillcolor=COLOR_TEAL,
            ),
            decreasing=dict(
                line=dict(color=COLOR_RED, width=1.2),
                fillcolor=COLOR_RED,
            ),
        ),
        row=1,
        col=1,
    )

    # 2. SMA Overlay (20-period) in amber
    if len(hist) >= 20:
        sma20 = calculate_sma(hist["Close"], window=20)
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=sma20,
                line=dict(color=COLOR_AMBER, width=1.6),
                name="SMA 20",
            ),
            row=1,
            col=1,
        )

    # 3. Volume Trace
    if "Volume" in hist.columns and not hist["Volume"].empty:
        volume_colors = [
            f"rgba(38, 166, 154, 0.65)" if row["Close"] >= row["Open"] else f"rgba(239, 83, 80, 0.65)"
            for _, row in hist.iterrows()
        ]
        fig.add_trace(
            go.Bar(
                x=hist.index,
                y=hist["Volume"],
                marker_color=volume_colors,
                name="Volume",
                showlegend=False,
            ),
            row=2,
            col=1,
        )

    # Layout styling
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL_BG,
        plot_bgcolor=CHART_BG,
        height=height,
        margin=dict(l=45, r=25, t=35, b=25),
        font=dict(family="Inter, -apple-system, sans-serif", color=COLOR_TEXT_PRIMARY, size=11),
        xaxis_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_TEXT_MUTED, size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=PANEL_BG,
            font_color=COLOR_TEXT_PRIMARY,
            bordercolor="rgba(232, 163, 61, 0.4)",
            font_size=11,
        ),
    )

    # Gridlines and axes
    for r in [1, 2]:
        fig.update_xaxes(
            gridcolor=COLOR_GRID,
            zerolinecolor=COLOR_ZERO,
            tickfont=dict(color=COLOR_TEXT_MUTED, size=10),
            row=r,
            col=1,
        )
        fig.update_yaxes(
            gridcolor=COLOR_GRID,
            zerolinecolor=COLOR_ZERO,
            tickfont=dict(color=COLOR_TEXT_MUTED, size=10),
            title_font=dict(color=COLOR_TEXT_MUTED, size=11),
            row=r,
            col=1,
        )

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    # Subplot annotation titles color
    for annotation in fig["layout"]["annotations"]:
        annotation["font"] = dict(color=COLOR_TEXT_PRIMARY, size=13, family="Inter, sans-serif")

    st.plotly_chart(fig, key=key, width="stretch")


def render_normalized_comparison(
    df,
    title: str = "Cross-Market Normalized Performance (%)",
    key: str | None = None,
) -> None:
    """Render a multi-instrument relative % performance line chart."""
    if df.empty:
        st.info("Not enough historical data for comparison chart.")
        return

    terminal_palette = [
        COLOR_AMBER,
        COLOR_TEAL,
        "#42A5F5",  # Blue
        COLOR_RED,
        "#AB47BC",  # Purple
        "#26C6DA",  # Cyan
        "#FFA726",  # Light orange
    ]

    fig = px.line(
        df,
        labels={"index": "Date", "value": "Return %", "variable": "Instrument"},
        color_discrete_sequence=terminal_palette,
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL_BG,
        plot_bgcolor=CHART_BG,
        height=380,
        margin=dict(l=45, r=25, t=30, b=25),
        font=dict(family="Inter, -apple-system, sans-serif", color=COLOR_TEXT_PRIMARY, size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_TEXT_MUTED, size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=PANEL_BG,
            font_color=COLOR_TEXT_PRIMARY,
            bordercolor="rgba(232, 163, 61, 0.4)",
            font_size=11,
        ),
    )

    fig.update_xaxes(gridcolor=COLOR_GRID, zerolinecolor=COLOR_ZERO, tickfont=dict(color=COLOR_TEXT_MUTED, size=10))
    fig.update_yaxes(
        gridcolor=COLOR_GRID,
        zerolinecolor=COLOR_ZERO,
        tickfont=dict(color=COLOR_TEXT_MUTED, size=10),
        title_font=dict(color=COLOR_TEXT_MUTED, size=11),
    )
    fig.add_hline(y=0, line_dash="dot", line_color=COLOR_TEXT_MUTED, opacity=0.7)

    st.plotly_chart(fig, key=key, width="stretch")
