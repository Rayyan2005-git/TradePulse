import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            .metric-card {
                background-color: #1E1E1E;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #333;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                margin-bottom: 8px;
            }
            .metric-label {
                font-size: 14px;
                color: #888;
            }
            .metric-value {
                font-size: 32px;
                font-weight: bold;
                color: #FFF;
            }
            .metric-delta {
                font-size: 16px;
            }
            .positive { color: #4CAF50; }
            .negative { color: #F44336; }
            .freshness-bar {
                font-size: 13px;
                color: #aaa;
                padding: 8px 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
