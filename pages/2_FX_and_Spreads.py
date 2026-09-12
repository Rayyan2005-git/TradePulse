"""TradePulse — FX and Currency Spreads Dashboard."""

from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick, render_normalized_comparison
from ui.page_utils import setup_page

st.set_page_config(
    page_title="TradePulse - FX & Spreads",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_autorefresh(interval=60000, limit=1000, key="data_refresh_fx")

snapshot, instruments, period, interval = setup_page(category="fx")

st.markdown('<span class="page-badge">FOREIGN EXCHANGE DESK</span>', unsafe_allow_html=True)
st.title("💱 FX & Currency Spreads")
st.markdown("Foreign exchange rates and dollar strength indicators (USD/INR and UUP ETF).")

quotes = DashboardService.ordered_quotes(snapshot, instruments)
render_metric_row(quotes)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 1-Day Change Summary")
    spread_df = DashboardService.spread_summary(snapshot)
    if not spread_df.empty:
        st.dataframe(spread_df, width="stretch", hide_index=True)
    else:
        st.info("No FX summary data available.")

with col2:
    st.subheader(f"📊 Relative Performance ({period})")
    comparison_df = DashboardService.comparison_dataframe(snapshot)
    if not comparison_df.empty:
        render_normalized_comparison(comparison_df)
    else:
        st.info("No comparison series available.")

st.markdown("---")

# Detailed Candlestick Charts in Tabs
st.subheader(f"📈 Currency Movement Analysis ({period})")

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
    st.info("No candlestick data available.")
