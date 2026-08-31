from datetime import datetime, timezone

from src.extract import fetch_klines
from DE_P.src.kline_process import process_klines
from src.load import load_to_neon


# Test one symbol first
symbol = ["BTCUSDT","ETHUSDT","SOLUSDT"]
interval = "1m"
batch_id = "integration_test_001"
ingested_at = datetime.now(timezone.utc)


# 1. Extract
print(f"\nFetching {symbol}...")

raw_klines = fetch_klines(
    symbol=symbol,
    interval=interval,
    limit=10
)

if raw_klines is None:
    print("Extraction failed.")
    raise SystemExit(1)

print(f"Raw records received: {len(raw_klines)}")


# 2. Transform + Validate
clean, quarantined = process_klines(
    symbol=symbol,
    raw_klines=raw_klines,
    interval=interval,
    batch_id=batch_id,
    ingested_at=ingested_at
)

print(f"Clean records: {len(clean)}")
print(f"Quarantined records: {len(quarantined)}")


# 3. Load clean records into Neon
if clean:
    load_to_neon(clean)
else:
    print("No clean records to load.")


# 4. Show quarantine information
if quarantined:
    print("\nQuarantined records:")

    for item in quarantined:
        print(item["reason"])


print("\nPipeline test completed.") 