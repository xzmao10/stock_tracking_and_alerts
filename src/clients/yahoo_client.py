"""Yahoo Finance client using yfinance.

This replaces the previous HTTP-based fetch with yfinance.Ticker calls.
"""
from typing import Optional, Dict, Any

try:
    import yfinance as yf
except Exception as exc:  # pragma: no cover - import-time
    yf = None

from ..errors import YahooAPIError


def fetch_quote(symbol: str) -> Dict[str, Any]:
    """Fetch quote info for a symbol using yfinance.

    Returns a dict with the raw yfinance info under key 'yf_info'.
    Raises ValueError for bad symbol input and YahooAPIError for fetch/import errors.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("symbol must be a non-empty string")

    if yf is None:
        raise YahooAPIError(
            "yfinance is not installed. Install it with: pip install yfinance"
        )

    try:
        t = yf.Ticker(symbol)
        info = t.info or {}
    except Exception as exc:
        raise YahooAPIError(f"Failed to fetch data from yfinance: {exc}") from exc

    return {"yf_info": info}


def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_stock_price(symbol: str) -> Dict[str, Any]:
    """Get normalized stock price information for a symbol using yfinance.

    Returns a dict with keys: symbol, price, currency, timestamp, raw
    """
    data = fetch_quote(symbol)
    info = data.get("yf_info", {})

    # Try common fields provided by yfinance
    price = _safe_float(
        info.get("regularMarketPrice")
        or info.get("currentPrice")
        or info.get("previousClose")
        or info.get("ask")
        or info.get("open")
    )

    currency = info.get("currency") or info.get("financialCurrency")
    timestamp = info.get("regularMarketTime")

    # Use symbol from info if available
    out_symbol = info.get("symbol") or symbol

    return {"symbol": out_symbol, "price": price, "currency": currency, "timestamp": timestamp, "raw": data}
