"""FX and cross-market summary."""

import streamlit as st

from services.dashboard import DashboardService
from ui.components.metric_card import render_metric_row
from ui.components.price_chart import render_candlestick
from ui.page_utils import setup_page

st.title("💱 FX & Spreads")
st.markdown("USD/INR and US Dollar Index")

snapshot, instruments, period, _ = setup_page(category="fx")

quotes = DashboardService.ordered_quotes(snapshot, instruments)
render_metric_row(quotes)

st.markdown("---")
st.subheader("Daily change summary")
spread_df = DashboardService.spread_summary(snapshot)
if not spread_df.empty:
    st.dataframe(spread_df, use_container_width=True, hide_index=True)
else:
    st.info("No FX data available.")

st.markdown("---")
st.subheader(f"FX charts ({period})")

for inst in instruments:
    series = snapshot.series.get(inst.id)
    if series:
        st.markdown(f"#### {inst.name}")
        render_candlestick(series)
