import plotly.graph_objects as go
import streamlit as st

from domain.models import InstrumentSeries


def render_candlestick(series: InstrumentSeries, height: int = 500) -> None:
    if not series.is_valid:
        st.info("No historical data available to display chart.")
        if series.error:
            st.caption(series.error)
        return

    hist = series.history
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            name=series.name,
        )
    )
    fig.update_layout(
        title=f"{series.name} — Price Movement",
        yaxis_title="Price",
        template="plotly_dark",
        height=height,
        xaxis_rangeslider_visible=False,
    )
    st.plotly_chart(fig, use_container_width=True)


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
    st.plotly_chart(fig, use_container_width=True)
