import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    status=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods={"GET"},
    raise_on_status=True,
)

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
logger = logging.getLogger(__name__)


def fetch_klines(symbol: str, interval: str = "1m", limit: int = 10):
    """Fetch Binance OHLCV candles.

    This module intentionally performs no network or database work at import
    time; the orchestrator is responsible for invoking this function.
    """
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    logger.info("Fetching %s from Binance", symbol)

    try:
        response = session.get(BINANCE_KLINES_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info("Fetched %s candles for %s", len(data), symbol)
        return data
    except requests.exceptions.RequestException:
        logger.exception("Binance request failed for %s", symbol)
        raise
