"""Shared page orchestration utilities for TradePulse pages."""

import streamlit as st

from config.settings import DEFAULT_INTERVAL, DEFAULT_PERIOD
from services.dashboard import DashboardService
from services.market_data import get_cached_snapshot
from ui.components.sidebar import render_sidebar
from ui.components.status_bar import render_status_bar
from ui.styles import inject_global_styles


def setup_page(category: str | None = None) -> tuple:
    """
    Standardized page initialization for TradePulse:
    1. Injects global dark terminal styling.
    2. Renders intentional branded navigation & sidebar controls.
    3. Fetches cached market snapshot for the category instruments.
    4. Renders status/freshness bar.
    5. Returns (snapshot, instruments, period, interval).
    """
    inject_global_styles()
    period, interval, _ = render_sidebar()

    instruments = DashboardService.instruments_for_page(category)
    ids = DashboardService.instrument_ids(instruments)

    with st.spinner("Fetching terminal feed..."):
        snapshot = get_cached_snapshot(
            ids,
            period or DEFAULT_PERIOD,
            interval or DEFAULT_INTERVAL,
        )

    render_status_bar(snapshot)
    return snapshot, instruments, period, interval
