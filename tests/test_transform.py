from datetime import datetime, timezone
from decimal import Decimal

from src.transform import transform_kline, validate_kline


def test_transform_kline_converts_values_and_timestamps():
    ingested_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    raw = [1767225600000, "100", "110", "90", "105", "12.5", 1767225659999]

    record = transform_kline("BTCUSDT", "1m", raw, "batch-id", ingested_at)

    assert record["open"] == Decimal("100")
    assert record["volume"] == Decimal("12.5")
    assert record["open_time"].tzinfo == timezone.utc
    assert record["batch_id"] == "batch-id"


def test_validate_kline_rejects_invalid_high():
    record = {
        "high": Decimal("99"),
        "low": Decimal("90"),
        "open": Decimal("100"),
        "close": Decimal("95"),
        "volume": Decimal("1"),
        "open_time": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "close_time": datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc),
    }

    valid, reason = validate_kline(record)

    assert valid is False
    assert reason == "High is not the Highest price"
