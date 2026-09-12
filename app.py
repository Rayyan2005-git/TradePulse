"""TradePulse — Streamlit Market Dashboard Entrypoint."""

from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

import streamlit as st

# Attempt clean switch to 0_All_Markets.py as the primary overview page
try:
    st.switch_page("pages/0_All_Markets.py")
except Exception:
    pass

# Fallback overview if switch_page is not executed
from streamlit_autorefresh import st_autorefresh
from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick, render_normalized_comparison
from ui.page_utils import setup_page

st.set_page_config(
    page_title="TradePulse - All Markets",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_autorefresh(interval=60000, limit=1000, key="data_refresh_root")

snapshot, instruments, period, interval = setup_page(category=None)

st.markdown('<span class="page-badge">GLOBAL MONITOR</span>', unsafe_allow_html=True)
st.title("🌐 All Markets Overview")
st.markdown("Real-time pulse across Commodities, Currencies, Crypto, and Benchmark Equities.")

st.markdown("---")

# Top Movers
st.subheader("⚡ Top Movers (1-Day Change)")
top_col1, top_col2 = st.columns(2)

gainers = DashboardService.top_movers(snapshot, ascending=False, limit=2)
decliners = DashboardService.top_movers(snapshot, ascending=True, limit=2)

with top_col1:
    st.markdown("##### 🟢 Top Leaders")
    if gainers:
        render_metric_row(gainers, columns=len(gainers))
    else:
        st.info("No leader data available.")

with top_col2:
    st.markdown("##### 🔴 Top Laggards")
    if decliners:
        render_metric_row(decliners, columns=len(decliners))
    else:
        st.info("No laggard data available.")

st.markdown("---")

st.subheader(f"📊 Relative Performance Comparison ({period})")
comparison_df = DashboardService.comparison_dataframe(snapshot)
if not comparison_df.empty:
    render_normalized_comparison(comparison_df)

st.markdown("---")

quotes = DashboardService.ordered_quotes(snapshot, instruments)
st.subheader(f"Market Quotes ({len(quotes)})")
render_metric_row(quotes, max_cols=4)
