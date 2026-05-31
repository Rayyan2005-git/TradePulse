import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
INSTRUMENTS_PATH = ROOT_DIR / "config" / "instruments.yaml"

DEFAULT_PERIOD = os.getenv("DEFAULT_PERIOD", "1mo")
DEFAULT_INTERVAL = os.getenv("DEFAULT_INTERVAL", "1d")
QUOTE_CACHE_TTL = int(os.getenv("QUOTE_CACHE_TTL", "120"))
HISTORY_CACHE_TTL = int(os.getenv("HISTORY_CACHE_TTL", "600"))
DATA_SOURCE_LABEL = "Yahoo Finance (via yfinance)"
