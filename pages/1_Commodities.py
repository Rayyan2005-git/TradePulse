"""Commodities — gold and crude oil."""

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick
from ui.page_utils import setup_page

st.title("🛢️ Commodities")
st.markdown("Gold and crude oil futures")

st_autorefresh(interval=60000, limit=1000, key="data_refresh_commodities")

snapshot, instruments, period, _ = setup_page(category="commodity")

quotes = DashboardService.ordered_quotes(snapshot, instruments)
render_metric_row(quotes)

st.markdown("---")
st.subheader(f"Candlestick charts ({period})")

for inst in instruments:
    series = snapshot.series.get(inst.id)
    if series:
        st.markdown(f"#### {inst.name}")
        render_candlestick(series)
