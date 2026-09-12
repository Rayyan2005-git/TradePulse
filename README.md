# TradePulse ⚡ — Multi-Asset Trading Terminal

A modular, high-performance Streamlit market dashboard providing real-time technical analysis and performance tracking across **Commodities**, **Foreign Exchange**, **Digital Assets**, and **Benchmark Equities** (powered by Yahoo Finance via `yfinance`).

---

## 🌟 Key Features

- **Trading Terminal Aesthetic**: High-contrast, dark institutional theme with deep navy/charcoal backgrounds (`#0B0E14` / `#131722`), amber/gold accents (`#E8A33D`), muted teal positive deltas (`#26A69A`), and soft red negative deltas (`#EF5350`).
- **Cross-Market Intelligence**: Top Movers engine ranking daily leaders and laggards across all tracked markets.
- **Interactive Candlestick & Volume Charts**: Plotly candlestick charts with 20-period Simple Moving Average (SMA-20) overlay and volume histograms.
- **Normalized Performance Comparison**: Multi-asset percentage return curves normalized over configurable timeframes.
- **Structured Multi-Page Navigation**: Branded sidebar navigation with custom status indicators, period controls, and instant cache invalidation.
- **Resilient Caching & Data Pipeline**: Thread-pooled data fetching with `@st.cache_data` caching and automatic 60-second refreshes.

---

## 📊 Market Desks & Instruments

| Desk | Instruments | Symbols | Currency | Description |
| :--- | :--- | :--- | :--- | :--- |
| 🌐 **All Markets** | All Instruments | — | — | Cross-asset overview, top movers, relative performance, and portfolio drilldowns |
| 🛢️ **Commodities** | Gold & WTI Crude Oil | `GC=F`, `CL=F` | USD | Global energy and precious metals futures |
| 💱 **FX & Spreads** | USD/INR & US Dollar Index | `INR=X`, `UUP` | INR, USD | Foreign currency rates and dollar strength indicators |
| 🪙 **Crypto** | Bitcoin Spot | `BTC-USD` | USD | 24h stats (High, Low, Volume) and spot candlestick momentum |
| 📈 **Stocks & Indices** | Nifty 50 & BSE Sensex | `^NSEI`, `^BSESN` | INR | Indian equity market bellwether indices |

---

## 🏗️ Architecture

The codebase follows clean architecture principles with distinct separation of concerns:

```
TradePulse/
├── app.py                     # Streamlit root entrypoint & route coordinator
├── pages/                     # Dedicated market desk pages
│   ├── 0_All_Markets.py       # Cross-market overview & top movers
│   ├── 1_Commodities.py       # Energy & precious metals desk
│   ├── 2_FX_and_Spreads.py    # FX rates & spread desk
│   ├── 3_Crypto.py            # Digital assets desk (Bitcoin)
│   └── 4_Stocks.py            # Indian benchmark indices desk
├── ui/                        # User interface layer
│   ├── styles.py              # Global terminal CSS injections & shimmer loaders
│   ├── page_utils.py          # Shared page bootstrap orchestration
│   └── components/            # Reusable UI widgets
│       ├── metric_card.py     # Terminal metric cards & responsive grid layout
│       ├── price_chart.py     # Plotly candlestick, SMA-20, & volume charts
│       ├── sidebar.py         # Custom branded navigation & control panel
│       └── status_bar.py      # Live status freshness bar & error badges
├── services/                  # Orchestration & caching layer
│   ├── dashboard.py           # Comparison dataframes, spreads, & top movers ranking
│   └── market_data.py         # Thread-pooled fetcher & @st.cache_data layer
├── domain/                    # Pure Python core models & analytics (zero UI deps)
│   ├── models.py              # Instrument, Quote, InstrumentSeries, MarketSnapshot
│   └── analytics.py           # change_abs, change_pct, calculate_sma, calculate_rsi
├── infrastructure/providers/  # External data adapter layer
│   ├── base.py                # MarketDataProvider Protocol
│   └── yfinance_provider.py   # Yahoo Finance provider with SSL resilience
├── config/                    # Configuration & settings
│   ├── instruments.yaml       # Market instrument registry
│   ├── settings.py            # App defaults & cache TTLs
│   └── ssl_fix.py             # SSL certificate bundle patch
└── tests/                     # Automated unit test suite
    └── test_analytics.py      # Core domain analytics tests
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (Python 3.11, 3.12, 3.13, 3.14 supported)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Rayyan2005-git/TradePulse.git
cd TradePulse

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
# Launch Streamlit app
python -m streamlit run app.py
```

Open the local URL displayed in the terminal (typically `http://localhost:8501`).

---

## ⚙️ Configuration

### Adding Instruments
To add new markets, update [`config/instruments.yaml`](config/instruments.yaml):

```yaml
  - id: eth
    name: Ethereum
    symbol: ETH-USD
    category: crypto
    currency: USD
    price_format: "${:,.2f}"
```

The app automatically detects the new instrument in the appropriate desk and the All Markets overview.

### Environment Variables
- `DEFAULT_PERIOD`: Default chart history period (default: `1mo`, options: `5d`, `1mo`, `3mo`, `6mo`, `1y`)
- `DEFAULT_INTERVAL`: Default candlestick interval (default: `1d`, options: `1d`, `1h`)
- `QUOTE_CACHE_TTL`: Price quote cache duration in seconds (default: `120`)
- `HISTORY_CACHE_TTL`: Historical candlestick series cache duration in seconds (default: `600`)

---

## 🧪 Testing

Run the domain analytics test suite:

```bash
python -m unittest discover tests
```

---

## ⚠️ Data Disclaimer

Market data is retrieved from Yahoo Finance via `yfinance` and is subject to exchange delays (typically 15 minutes). This platform is built for educational, analytical, and portfolio tracking purposes, not for high-frequency or automated trade execution.
