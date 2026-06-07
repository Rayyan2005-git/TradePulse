import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            /* Premium Glassmorphism Theme */
            .metric-card {
                background: rgba(30, 30, 30, 0.6);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                padding: 24px;
                margin-bottom: 12px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .metric-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            .metric-label {
                font-family: 'Inter', sans-serif;
                font-size: 15px;
                font-weight: 500;
                color: #A0AAB4;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .metric-value {
                font-family: 'Inter', sans-serif;
                font-size: 36px;
                font-weight: 700;
                color: #FFFFFF;
                margin-bottom: 8px;
            }
            .metric-delta {
                font-family: 'Inter', sans-serif;
                font-size: 16px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            .positive { 
                color: #00E676; /* Vibrant Green */
            }
            .negative { 
                color: #FF1744; /* Vibrant Red */
            }
            .positive-bg {
                background: rgba(0, 230, 118, 0.1);
                padding: 4px 8px;
                border-radius: 6px;
            }
            .negative-bg {
                background: rgba(255, 23, 68, 0.1);
                padding: 4px 8px;
                border-radius: 6px;
            }
            .freshness-bar {
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                color: #6c757d;
                padding: 8px 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
