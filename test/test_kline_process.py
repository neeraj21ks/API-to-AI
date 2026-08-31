from datetime import datetime, timezone
from DE_P.src.kline_process import process_klines

# Sample raw Binance kline
raw_klines = [
    [
        1756296000000,       # open_time
        "78898.58",          # open
        "78904.72",          # high
        "78852.28",          # low
        "78883.99",          # close
        "5.00609",           # volume
        1756296059999,       # close_time
        "0",                 # quote asset volume
        100,                 # number of trades
        "0",                 # taker buy base volume
        "0",                 # taker buy quote volume
        "0"                  # ignore
    ]
]


batch_id = "test_batch_001"

ingested_at = datetime.now(timezone.utc)


clean, quarantined = process_klines(
    symbol="BTCUSDT",
    raw_klines=raw_klines,
    interval="1m",
    batch_id=batch_id,
    ingested_at=ingested_at
)

print("CLEAN:")
print(clean)

print("\nQUARANTINED:")
print(quarantined)

print("\nClean records:", len(clean))
print("Quarantined records:", len(quarantined))

#test 1: valid candle

valid_raw_klines = [
    [
        1756296000000,
        "78898.58",
        "78904.72",
        "78852.28",
        "78883.99",
        "5.00609",
        1756296059999,
        "0",
        100,
        "0",
        "0",
        "0"
    ]
]

batch_id = "test_batch_001"
ingested_at = datetime.now(timezone.utc)

clean, quarantined = process_klines(
    "BTCUSDT",
    valid_raw_klines,
    "1m",
    batch_id,
    ingested_at
)

print("VALID TEST")
print("Clean records:", len(clean))
print("Quarantined records:", len(quarantined))

# test 2: Invalid candle

invalid_raw_klines = [
    [
        1756296060000,
        "78898.58",
        "78850.00",       # INVALID: high < close
        "78852.28",
        "78883.99",
        "5.00609",
        1756296119999,
        "0",
        100,
        "0",
        "0",
        "0"
    ]
]

clean, quarantined = process_klines(
    "BTCUSDT",
    invalid_raw_klines,
    "1m",
    batch_id,
    ingested_at
)

print("\nINVALID TEST")
print("Clean records:", len(clean))
print("Quarantined records:", len(quarantined))
print("Reason:", quarantined[0]["reason"])