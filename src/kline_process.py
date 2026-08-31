from datetime import datetime, timezone
from decimal import Decimal
from collections import defaultdict

from src.transform import transform_kline, validate_kline  # Replace with your actual module

def process_klines(symbol, raw_klines, interval, batch_id, ingested_at):

    clean = []
    quarantined = []

    for raw_candle in raw_klines:

        try:
            record = transform_kline(
                symbol,
                interval,
                raw_candle,
                batch_id,
                ingested_at
            )

            valid, reason = validate_kline(record)

            if valid:
                clean.append(record)
            else:
                quarantined.append({
                    "record": record,
                    "reason": reason
                })

        except Exception as e:
            quarantined.append({
                "record": raw_candle,
                "reason": f"TRANSFORMATION_ERROR: {str(e)}"
            })

    return clean, quarantined