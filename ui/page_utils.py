import streamlit as st

from config.settings import DEFAULT_INTERVAL, DEFAULT_PERIOD
from services.dashboard import DashboardService
from services.market_data import get_cached_snapshot
from ui.components.status_bar import render_sidebar_controls, render_status_bar
from ui.styles import inject_global_styles


def setup_page(category: str | None = None) -> tuple:
    """Shared page setup; returns (snapshot, instruments, period, interval)."""
    inject_global_styles()
    period, interval, _ = render_sidebar_controls()
    instruments = DashboardService.instruments_for_page(category)
    ids = DashboardService.instrument_ids(instruments)

    with st.spinner("Loading market snapshot…"):
        snapshot = get_cached_snapshot(
            ids,
            period or DEFAULT_PERIOD,
            interval or DEFAULT_INTERVAL,
        )

    render_status_bar(snapshot)
    return snapshot, instruments, period, interval
