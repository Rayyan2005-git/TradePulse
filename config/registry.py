from pathlib import Path
from typing import List, Optional

import yaml

from config.settings import INSTRUMENTS_PATH
from domain.models import Instrument


def load_instruments(path: Optional[Path] = None) -> List[Instrument]:
    config_path = path or INSTRUMENTS_PATH
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return [
        Instrument(
            id=item["id"],
            name=item["name"],
            symbol=item["symbol"],
            category=item["category"],
            currency=item["currency"],
            price_format=item["price_format"],
        )
        for item in data["instruments"]
    ]


def filter_by_category(instruments: List[Instrument], category: str) -> List[Instrument]:
    return [i for i in instruments if i.category == category]
