#test case:1  valid BTC candle

from datetime import datetime,timezone
from decimal import Decimal
from src.transform import validate_kline, validate_sequence,validate_duplicates,transform_kline,transform_and_validate

def test_transform_kline():

    raw_kline = [
        1724600000000,
        "100.00",
        "105.00",
        "99.00",
        "103.00",
        "25.50",
        1724600059999,
        "2550.00",
        100,
        "12.75",
        "1275.00",
        "0"
    ]

    ingested_at = datetime.now(timezone.utc)

    record = transform_kline(
        symbol="BTCUSDT",
        interval="1m",
        kline=raw_kline,
        batch_id="test_batch_001",
        ingested_at=ingested_at
    )

    assert record["symbol"] == "BTCUSDT"
    assert record["interval"] == "1m"
    assert record["source"] == "binance"

    assert record["open"] == Decimal("100.00")
    assert record["high"] == Decimal("105.00")
    assert record["low"] == Decimal("99.00")
    assert record["close"] == Decimal("103.00")
    assert record["volume"] == Decimal("25.50")

    assert record["open_time"].tzinfo == timezone.utc
    assert record["close_time"].tzinfo == timezone.utc

    assert record["batch_id"] == "test_batch_001"
    assert record["ingested_at"] == ingested_at

#test case:2  valid candle passes validation

def test_valid_kline():

    record = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 30,
            tzinfo=timezone.utc
        ),
        "close_time": datetime(
            2026, 8, 26, 12, 30, 59,
            tzinfo=timezone.utc
        ),
        "open": Decimal("100"),
        "high": Decimal("105"),
        "low": Decimal("99"),
        "close": Decimal("103"),
        "volume": Decimal("10"),
    }

    valid, reason = validate_kline(record)

    assert valid is True
    assert reason is None

#test case:3  invalid high

def test_invalid_high():

    record = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 30,
            tzinfo=timezone.utc
        ),
        "close_time": datetime(
            2026, 8, 26, 12, 30, 59,
            tzinfo=timezone.utc
        ),
        "open": Decimal("100"),
        "high": Decimal("95"),
        "low": Decimal("90"),
        "close": Decimal("94"),
        "volume": Decimal("10"),
    }

    valid, reason = validate_kline(record)

    assert valid is False
    assert reason == "High is not the Highest price"

#test case:4  negative volume

def test_negative_volume():

    record = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 30,
            tzinfo=timezone.utc
        ),
        "close_time": datetime(
            2026, 8, 26, 12, 30, 59,
            tzinfo=timezone.utc
        ),
        "open": Decimal("100"),
        "high": Decimal("105"),
        "low": Decimal("99"),
        "close": Decimal("103"),
        "volume": Decimal("-10"),
    }

    valid, reason = validate_kline(record)

    assert valid is False
    assert reason == "Volume can't be Negative"

#test case:5  duplicate detection

def test_duplicate_detection():

    record_1 = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 30,
            tzinfo=timezone.utc
        )
    }

    record_2 = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 31,
            tzinfo=timezone.utc
        )
    }

    record_3 = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 31,
            tzinfo=timezone.utc
        )
    }

    issues = validate_duplicates([
        record_1,
        record_2,
        record_3
    ])

    assert len(issues) == 1
    assert issues[0]["type"] == "duplicate"
    assert issues[0]["timestamp"] == record_3["open_time"]

#test case:6  gap detection

def test_sequence_gap():

    records = [
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 31,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 34,
                tzinfo=timezone.utc
            )
        }
    ]

    issues = validate_sequence(records)

    assert len(issues) == 1

    assert issues[0]["type"] == "gap"
    assert issues[0]["symbol"] == "BTCUSDT"
    assert issues[0]["interval"] == "1m"
    assert issues[0]["missing_candles"] == 2

#test case:7  close_time <= open_time, invalid close time

def test_invalid_close_time():

    record = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "open_time": datetime(
            2026, 8, 26, 12, 30,
            tzinfo=timezone.utc
        ),
        "close_time": datetime(
            2026, 8, 26, 12, 30,
            tzinfo=timezone.utc
        ),
        "open": Decimal("100"),
        "high": Decimal("105"),
        "low": Decimal("99"),
        "close": Decimal("103"),
        "volume": Decimal("10"),
    }

    valid, reason = validate_kline(record)

    assert valid is False
    assert reason == "close_time is not after open_time"

#test case:8  duplicate candle.don't duplicate the duplicate test

def test_duplicate_detection_different_symbols():

    records = [
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "ETHUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        }
    ]

    issues = validate_duplicates(records)

    assert issues == []

#test case:9  one-minute gap, exact one-minute gap

def test_sequence_one_minute_gap():

    records = [
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 32,
                tzinfo=timezone.utc
            )
        }
    ]

    issues = validate_sequence(records)

    assert len(issues) == 1
    assert issues[0]["type"] == "gap"
    assert issues[0]["missing_candles"] == 1

#test case:10 multiple symbols

def test_sequence_multiple_symbols():

    records = [
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 31,
                tzinfo=timezone.utc
            ),
        },
        {
            "symbol": "ETHUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            ),
        },
        {
            "symbol": "ETHUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 31,
                tzinfo=timezone.utc
            ),
        },
    ]

    issues = validate_sequence(records)

    assert issues == []

#test case:11 multiple intervals

def test_sequence_multiple_intervals():

    records = [
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "open_time": datetime(
                2026, 8, 26, 12, 31,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "5m",
            "open_time": datetime(
                2026, 8, 26, 12, 30,
                tzinfo=timezone.utc
            )
        },
        {
            "symbol": "BTCUSDT",
            "interval": "5m",
            "open_time": datetime(
                2026, 8, 26, 12, 35,
                tzinfo=timezone.utc
            )
        },
    ]

    issues = validate_sequence(records)

    assert issues == []

#test case:12 empty input

def test_empty_input():

    clean, quarantined = transform_and_validate(
        symbol="BTCUSDT",
        raw_klines=[],
        interval="1m",
        batch_id="test_batch",
        ingested_at=datetime.now(timezone.utc)
    )

    assert clean == []
    assert quarantined == []

def test_empty_sequence():

    issues = validate_sequence([])

    assert issues == []

#test case:13 — malformed raw candle is quarantined

def test_malformed_kline_is_quarantined():

    malformed_kline = [
        1724600000000,
        "100.00",
        "105.00",
        # low missing
        "103.00",
        "25.50"
    ]

    clean, quarantined = transform_and_validate(
        symbol="BTCUSDT",
        raw_klines=[malformed_kline],
        interval="1m",
        batch_id="test_batch",
        ingested_at=datetime.now(timezone.utc)
    )

    assert clean == []
    assert len(quarantined) == 1
    assert quarantined[0]["record"] == malformed_kline
    assert quarantined[0]["reason"].startswith(
        "TRANSFORMATION_ERROR:"
    )

