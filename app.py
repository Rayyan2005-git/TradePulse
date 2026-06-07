"""TradePulse — IIFT Analyst Dashboard (Overview)."""

from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick, render_normalized_comparison
from ui.page_utils import setup_page

st.set_page_config(
    page_title="TradePulse - Overview",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚡ TradePulse")
st.markdown("### IIFT Analyst Dashboard — Market Snapshot")
st.caption("Delayed market data · Auto-refreshes every 60s")

# Auto-refresh every 60 seconds (60000 milliseconds)
st_autorefresh(interval=60000, limit=1000, key="data_refresh")

snapshot, instruments, period, interval = setup_page()

quotes = DashboardService.ordered_quotes(snapshot, instruments)
render_metric_row(quotes)

st.markdown("---")
st.subheader("Normalized comparison")
comparison_df = DashboardService.comparison_dataframe(snapshot)
render_normalized_comparison(comparison_df)

st.markdown("---")
st.subheader(f"Price charts ({period})")
valid_ids = [
    i.id
    for i in instruments
    if i.id in snapshot.series and snapshot.series[i.id].is_valid
]
if valid_ids:
    tabs = st.tabs([snapshot.quotes[i].name for i in valid_ids])
    for tab, inst_id in zip(tabs, valid_ids):
        with tab:
            render_candlestick(snapshot.series[inst_id])
else:
    st.info("No chart data available.")
