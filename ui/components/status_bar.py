"""Status bar and freshness indicators for market data snapshots."""

import streamlit as st

from domain.models import MarketSnapshot
from ui.components.sidebar import render_sidebar


def render_status_bar(snapshot: MarketSnapshot) -> None:
    """Render a terminal freshness indicator bar with active pulse dot."""
    fetched = snapshot.fetched_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    status = f"{snapshot.success_count}/{snapshot.total_count} loaded"

    st.markdown(
        f"""
        <div class="freshness-bar">
            <span class="pulse-dot"></span>
            <span><strong>Snapshot Status:</strong> {status}</span>
            <span>·</span>
            <span><strong>Updated:</strong> {fetched}</span>
            <span>·</span>
            <span><strong>Period:</strong> {snapshot.period} ({snapshot.interval})</span>
            <span>·</span>
            <span><strong>Source:</strong> {snapshot.source}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if snapshot.load_errors:
        with st.expander(f"⚠️ Feed Alerts ({len(snapshot.load_errors)})", expanded=False):
            for err in snapshot.load_errors:
                st.warning(err)


def render_sidebar_controls() -> tuple[str, str, bool]:
    """Compatibility wrapper delegating to modern render_sidebar."""
    return render_sidebar()
