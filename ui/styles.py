"""Global styles and CSS injections for the TradePulse trading terminal theme."""

import streamlit as st


def inject_global_styles() -> None:
    """Inject cohesive dark terminal CSS with amber, teal, and red accents."""
    st.markdown(
        """
        <style>
            /* 1. Root and Global App Styling */
            .stApp {
                background-color: #0B0E14;
                color: #E8E8E8;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }

            /* 2. Card Layout for Metrics */
            .metric-card {
                background: #131722;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
                padding: 20px;
                margin-bottom: 12px;
                transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
                border: 1px solid rgba(232, 163, 61, 0.35);
            }
            .metric-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }
            .metric-label {
                font-size: 13px;
                font-weight: 600;
                color: #8A8D93;
                text-transform: uppercase;
                letter-spacing: 0.6px;
            }
            .metric-symbol-badge {
                font-size: 11px;
                color: #8A8D93;
                background: rgba(255, 255, 255, 0.05);
                padding: 2px 6px;
                border-radius: 4px;
                font-weight: 500;
            }
            .metric-value {
                font-size: 28px;
                font-weight: 700;
                color: #E8E8E8;
                letter-spacing: -0.5px;
                margin-bottom: 8px;
                font-variant-numeric: tabular-nums;
            }
            .metric-delta {
                font-size: 13px;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 5px;
                padding: 3px 8px;
                border-radius: 6px;
                font-variant-numeric: tabular-nums;
            }
            .positive { 
                color: #26A69A; /* Muted Teal-Green */
            }
            .negative { 
                color: #EF5350; /* Soft Red */
            }
            .positive-bg {
                background: rgba(38, 166, 154, 0.12);
                color: #26A69A;
            }
            .negative-bg {
                background: rgba(239, 83, 80, 0.12);
                color: #EF5350;
            }

            /* 3. Skeleton Loading Shimmer */
            @keyframes shimmer {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
            .skeleton-card {
                background: linear-gradient(90deg, #131722 25%, #1c2230 50%, #131722 75%);
                background-size: 200% 100%;
                animation: shimmer 1.5s infinite;
                border-radius: 12px;
                height: 125px;
                border: 1px solid rgba(255, 255, 255, 0.05);
                margin-bottom: 12px;
            }

            /* 4. Intentional Sidebar Navigation */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            [data-testid="stSidebar"] {
                background-color: #131722 !important;
                border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
            }
            .sidebar-brand-container {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 10px 4px 16px 4px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                margin-bottom: 16px;
            }
            .sidebar-brand-icon {
                font-size: 22px;
            }
            .sidebar-brand-title {
                font-size: 18px;
                font-weight: 700;
                color: #E8E8E8;
                letter-spacing: -0.5px;
            }
            .sidebar-brand-badge {
                background: rgba(232, 163, 61, 0.15);
                color: #E8A33D;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 6px;
                border-radius: 4px;
                letter-spacing: 0.5px;
                border: 1px solid rgba(232, 163, 61, 0.3);
            }
            .sidebar-nav-title {
                font-size: 11px;
                font-weight: 600;
                color: #8A8D93;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin: 14px 0 6px 4px;
            }
            [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
                background-color: transparent !important;
                color: #E8E8E8 !important;
                border-radius: 8px !important;
                padding: 8px 12px !important;
                margin-bottom: 3px !important;
                border-left: 3px solid transparent !important;
                transition: all 0.2s ease !important;
                text-decoration: none !important;
                font-weight: 500 !important;
                font-size: 14px !important;
            }
            [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
                background-color: rgba(232, 163, 61, 0.08) !important;
                color: #E8A33D !important;
                border-left: 3px solid rgba(232, 163, 61, 0.5) !important;
            }
            [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
                background-color: rgba(232, 163, 61, 0.12) !important;
                color: #E8A33D !important;
                border-left: 3px solid #E8A33D !important;
                font-weight: 600 !important;
            }

            /* 5. Status Pill & Pulsing Dot */
            .status-pill {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                background: rgba(38, 166, 154, 0.1);
                border: 1px solid rgba(38, 166, 154, 0.25);
                padding: 4px 10px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 600;
                color: #26A69A;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            }
            .pulse-dot {
                width: 7px;
                height: 7px;
                background-color: #26A69A;
                border-radius: 50%;
                box-shadow: 0 0 0 rgba(38, 166, 154, 0.6);
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(38, 166, 154, 0.7); }
                70% { box-shadow: 0 0 0 6px rgba(38, 166, 154, 0); }
                100% { box-shadow: 0 0 0 0 rgba(38, 166, 154, 0); }
            }
            .freshness-bar {
                font-size: 12px;
                color: #8A8D93;
                padding: 6px 0 12px 0;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            /* 6. Tabs & Dataframe Styling */
            button[data-baseweb="tab"] {
                color: #8A8D93 !important;
                font-weight: 500 !important;
                font-size: 14px !important;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #E8A33D !important;
                font-weight: 600 !important;
                border-bottom-color: #E8A33D !important;
            }
            div[data-baseweb="tab-highlight"] {
                background-color: #E8A33D !important;
            }
            div[data-testid="stDataFrame"] {
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 10px !important;
                overflow: hidden !important;
            }

            /* 7. Controls & Buttons */
            button[kind="secondary"] {
                background-color: #131722 !important;
                border: 1px solid rgba(232, 163, 61, 0.3) !important;
                color: #E8A33D !important;
                font-weight: 500 !important;
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }
            button[kind="secondary"]:hover {
                background-color: rgba(232, 163, 61, 0.15) !important;
                border-color: #E8A33D !important;
                color: #FFFFFF !important;
            }

            /* 8. Accent Headers */
            h1, h2, h3 {
                color: #E8E8E8 !important;
                font-weight: 700 !important;
            }
            .page-badge {
                display: inline-block;
                background: rgba(232, 163, 61, 0.12);
                color: #E8A33D;
                font-size: 11px;
                font-weight: 600;
                padding: 2px 8px;
                border-radius: 4px;
                letter-spacing: 0.5px;
                margin-bottom: 6px;
                border: 1px solid rgba(232, 163, 61, 0.25);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
