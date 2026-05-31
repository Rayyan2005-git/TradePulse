import streamlit as st

from domain.models import MarketSnapshot


def render_status_bar(snapshot: MarketSnapshot) -> None:
    fetched = snapshot.fetched_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    status = f"{snapshot.success_count}/{snapshot.total_count} instruments loaded"
    st.markdown(
        f'<p class="freshness-bar">'
        f"Snapshot: {status} · Fetched {fetched} · "
        f"Period: {snapshot.period} · Source: {snapshot.source}"
        f"</p>",
        unsafe_allow_html=True,
    )
    if snapshot.load_errors:
        with st.expander("Load warnings", expanded=False):
            for err in snapshot.load_errors:
                st.warning(err)


def render_sidebar_controls() -> tuple[str, str, bool]:
    st.sidebar.header("Controls")
    period = st.sidebar.selectbox(
        "History period",
        options=["5d", "1mo", "3mo", "6mo", "1y"],
        index=1,
    )
    interval = st.sidebar.selectbox(
        "Interval",
        options=["1d", "1h"],
        index=0,
    )
    refresh = st.sidebar.button("Refresh data", use_container_width=True)
    if refresh:
        st.cache_data.clear()
    return period, interval, refresh
