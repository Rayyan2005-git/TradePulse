"""Intentional custom sidebar navigation and controls component."""

import os
import streamlit as st


def _safe_page_link(page_path: str, label: str, icon: str) -> None:
    """Safely render st.page_link whether launched from root or subpage."""
    candidates = [
        page_path,
        os.path.basename(page_path),
        f"../{page_path}",
    ]
    for p in candidates:
        try:
            st.page_link(p, label=label, icon=icon)
            return
        except Exception:
            continue


def render_sidebar() -> tuple[str, str, bool]:
    """
    Renders intentional custom sidebar navigation, status pill, and controls.
    Returns (period, interval, refresh_clicked).
    """
    with st.sidebar:
        # 1. Brand header
        st.markdown(
            """
            <div class="sidebar-brand-container">
                <span class="sidebar-brand-icon">⚡</span>
                <span class="sidebar-brand-title">TradePulse</span>
                <span class="sidebar-brand-badge">TERMINAL</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Live status indicator
        st.markdown(
            """
            <div class="status-pill">
                <span class="pulse-dot"></span>
                <span>FEED CONNECTED · 60s REFRESH</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3. Custom Navigation
        st.markdown('<div class="sidebar-nav-title">Markets & Portfolios</div>', unsafe_allow_html=True)
        _safe_page_link("pages/0_All_Markets.py", label="All Markets Overview", icon="🌐")
        _safe_page_link("pages/1_Commodities.py", label="Commodities", icon="🛢️")
        _safe_page_link("pages/2_FX_and_Spreads.py", label="FX & Spreads", icon="💱")
        _safe_page_link("pages/3_Crypto.py", label="Crypto (Bitcoin)", icon="🪙")
        _safe_page_link("pages/4_Stocks.py", label="Stocks & Indices", icon="📈")

        st.markdown("---")

        # 4. Market Controls
        st.markdown('<div class="sidebar-nav-title">Terminal Controls</div>', unsafe_allow_html=True)
        period = st.selectbox(
            "History Period",
            options=["5d", "1mo", "3mo", "6mo", "1y"],
            index=1,
            key="tp_period_select",
        )
        interval = st.selectbox(
            "Interval",
            options=["1d", "1h"],
            index=0,
            key="tp_interval_select",
        )

        refresh = st.button("🔄 Clear Cache & Refresh", width="stretch")
        if refresh:
            st.cache_data.clear()
            st.rerun()

        st.caption("Data source: Yahoo Finance · Delayed snapshot")

    return period, interval, refresh
