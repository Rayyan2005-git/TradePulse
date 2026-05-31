# TradePulse — IIFT Analyst Dashboard

Modular Streamlit dashboard for commodity and FX market snapshots (Yahoo Finance via `yfinance`).

## Architecture

```
app.py / pages/          → Streamlit UI
ui/components/           → Reusable widgets
services/                → Market data orchestration + caching
domain/                  → Models and analytics (pure Python)
infrastructure/          → yfinance provider adapter
config/                  → instruments.yaml + settings
```

## Quick start

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## Pages

| Page | Description |
|------|-------------|
| **Overview** | All instruments, normalized comparison, charts |
| **Commodities** | Gold & crude oil |
| **FX & Spreads** | USD/INR, Dollar Index, change summary |

## Configuration

- **Instruments:** edit `config/instruments.yaml`
- **Cache TTL:** set env `QUOTE_CACHE_TTL` (default 120s)
- **Theme:** `.streamlit/config.toml`

## Sidebar

- Change history period and interval
- **Refresh data** clears cache and reloads

## Note on data

Data is **delayed** (Yahoo Finance). Not suitable for live trading decisions.
