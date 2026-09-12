"""TradePulse — Crypto Dashboard (Bitcoin Spot)."""

from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick
from ui.page_utils import setup_page

st.set_page_config(
    page_title="TradePulse - Crypto",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_autorefresh(interval=60000, limit=1000, key="data_refresh_crypto")

snapshot, instruments, period, interval = setup_page(category="crypto")

st.markdown('<span class="page-badge">DIGITAL ASSETS DESK</span>', unsafe_allow_html=True)
st.title("🪙 Crypto Desk — Bitcoin")
st.markdown("Spot cryptocurrency price action, momentum, and volume analysis for Bitcoin (BTC-USD).")

quotes = DashboardService.ordered_quotes(snapshot, instruments)
render_metric_row(quotes)

st.markdown("---")

# Quick Stats Row if history is available
btc_series = snapshot.series.get("btc")
if btc_series and btc_series.is_valid and not btc_series.history.empty:
    hist = btc_series.history
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Period High", f"${float(hist['High'].max()):,.2f}")
    with c2:
        st.metric("Period Low", f"${float(hist['Low'].min()):,.2f}")
    with c3:
        st.metric("Latest Close", f"${float(hist['Close'].iloc[-1]):,.2f}")
    with c4:
        vol = hist["Volume"].iloc[-1] if "Volume" in hist.columns else 0
        st.metric("24h Volume", f"{vol:,.0f}")

st.markdown("---")

st.subheader(f"📈 Bitcoin Price Action ({period})")

if btc_series and btc_series.is_valid:
    render_candlestick(btc_series)
else:
    st.info("No candlestick data available for Bitcoin.")

