"""TradePulse — Equities & Benchmark Indices Dashboard (Nifty 50 & Sensex)."""

from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick, render_normalized_comparison
from ui.page_utils import setup_page

st.set_page_config(
    page_title="TradePulse - Stocks & Indices",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_autorefresh(interval=60000, limit=1000, key="data_refresh_stocks")

snapshot, instruments, period, interval = setup_page(category="stocks")

st.markdown('<span class="page-badge">EQUITIES & INDICES DESK</span>', unsafe_allow_html=True)
st.title("📈 Benchmark Equities & Indices")
st.markdown("Indian equity bellwethers: NSE Nifty 50 (^NSEI) and BSE Sensex (^BSESN).")

quotes = DashboardService.ordered_quotes(snapshot, instruments)
render_metric_row(quotes)

st.markdown("---")

# Relative Performance Comparison
st.subheader(f"📊 Relative Performance Comparison ({period})")
comparison_df = DashboardService.comparison_dataframe(snapshot)
if not comparison_df.empty:
    render_normalized_comparison(comparison_df)
else:
    st.info("Insufficient index data for relative comparison.")

st.markdown("---")

# Detailed Candlestick Charts in Tabs
st.subheader(f"📈 Index Candlestick Charts ({period})")

valid_ids = [
    i.id for i in instruments
    if i.id in snapshot.series and snapshot.series[i.id].is_valid
]

if valid_ids:
    tabs = st.tabs([snapshot.quotes[i].name for i in valid_ids])
    for tab, inst_id in zip(tabs, valid_ids):
        with tab:
            render_candlestick(snapshot.series[inst_id])
else:
    st.info("No candlestick data available for benchmark indices.")

