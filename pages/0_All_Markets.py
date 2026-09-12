"""TradePulse — All Markets Overview (Cross-Category Dashboard)."""

from config.ssl_fix import apply_ssl_cert_bundle

apply_ssl_cert_bundle()

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick, render_normalized_comparison
from ui.page_utils import setup_page

st.set_page_config(
    page_title="TradePulse - All Markets",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_autorefresh(interval=60000, limit=1000, key="data_refresh_all_markets")

# Shared setup: styles, intentional sidebar, snapshot fetching, status bar
snapshot, instruments, period, interval = setup_page(category=None)

st.markdown('<span class="page-badge">GLOBAL MONITOR</span>', unsafe_allow_html=True)
st.title("🌐 All Markets Overview")
st.markdown("Real-time pulse across Commodities, Currencies, Crypto, and Benchmark Equities.")

st.markdown("---")

# 1. Top Movers Section
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

# 2. Cross-Market Normalized Comparison
st.subheader(f"📊 Relative Performance Comparison ({period})")
comparison_df = DashboardService.comparison_dataframe(snapshot)
if not comparison_df.empty:
    render_normalized_comparison(comparison_df)
else:
    st.info("Insufficient historical data for relative comparison.")

st.markdown("---")

# 3. Market Categories Deep Dive
st.subheader("🔍 Asset Class Portfolios")

categories = [
    ("All Markets", None),
    ("🛢️ Commodities", "commodity"),
    ("💱 FX & Currencies", "fx"),
    ("🪙 Crypto", "crypto"),
    ("📈 Stocks & Indices", "stocks"),
]

tabs = st.tabs([label for label, _ in categories])

for tab, (label, cat_filter) in zip(tabs, categories):
    with tab:
        cat_instruments = [
            i for i in instruments
            if cat_filter is None or i.category == cat_filter
        ]
        cat_quotes = DashboardService.ordered_quotes(snapshot, cat_instruments)
        
        st.markdown(f"#### Market Quotes ({len(cat_quotes)})")
        render_metric_row(cat_quotes, max_cols=4)

        valid_ids = [
            i.id for i in cat_instruments
            if i.id in snapshot.series and snapshot.series[i.id].is_valid
        ]

        if valid_ids:
            st.markdown(f"#### Detailed Charts ({period})")
            chart_tabs = st.tabs([snapshot.quotes[i].name for i in valid_ids])
            for ctab, inst_id in zip(chart_tabs, valid_ids):
                with ctab:
                    render_candlestick(snapshot.series[inst_id], key=f"candlestick_{cat_filter}_{inst_id}")
        else:
            st.info("No chart series available for this asset class.")

