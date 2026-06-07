import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from domain.models import InstrumentSeries
from domain.analytics import calculate_sma


def render_candlestick(series: InstrumentSeries, height: int = 600) -> None:
    if not series.is_valid:
        st.info("No historical data available to display chart.")
        if series.error:
            st.caption(series.error)
        return

    hist = series.history
    
    # Create subplots: 2 rows, 1 col. Top for price, bottom for volume.
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        subplot_titles=(f"{series.name} — Price Movement", "Volume"),
        row_width=[0.2, 0.7]  # Volume gets 20%, Price gets 70% of height
    )

    # 1. Candlestick Trace
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            name="Price",
        ),
        row=1, col=1
    )

    # 2. SMA Overlay (20-day)
    if len(hist) >= 20:
        sma20 = calculate_sma(hist["Close"], window=20)
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=sma20,
                line=dict(color='orange', width=1.5),
                name='SMA 20'
            ),
            row=1, col=1
        )

    # 3. Volume Trace
    if "Volume" in hist.columns:
        # Determine color for volume bars (green if close >= open, else red)
        colors = ['#00E676' if row['Close'] >= row['Open'] else '#FF1744' for index, row in hist.iterrows()]
        fig.add_trace(
            go.Bar(
                x=hist.index,
                y=hist["Volume"],
                marker_color=colors,
                name="Volume"
            ),
            row=2, col=1
        )

    fig.update_layout(
        template="plotly_dark",
        height=height,
        xaxis_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Update y-axis titles
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    st.plotly_chart(fig, width="stretch")


def render_normalized_comparison(df, title: str = "Normalized Performance (%)") -> None:
    import plotly.express as px

    if df.empty:
        st.info("Not enough data for comparison chart.")
        return

    fig = px.line(
        df,
        title=title,
        labels={"index": "Date", "value": "Return %", "variable": "Instrument"},
    )
    fig.update_layout(template="plotly_dark", height=400)
    fig.add_hline(y=0, line_dash="dot", line_color="#666")
    st.plotly_chart(fig, width="stretch")
