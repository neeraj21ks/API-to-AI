from datetime import datetime,timezone,timedelta
from decimal import Decimal
from collections import defaultdict

#Tradnsforming the raw data
def transform_kline(symbol,interval,kline,batch_id,ingested_at):
    record={"symbol":symbol,
            "open_time":datetime.fromtimestamp(kline[0]/1000,tz=timezone.utc),
            "close_time":datetime.fromtimestamp(kline[6]/1000,tz=timezone.utc),
            "open":Decimal(kline[1]),
            "high":Decimal(kline[2]),
            "low":Decimal(kline[3]),
            "close":Decimal(kline[4]),
            "volume":Decimal(kline[5]),
            "interval":interval,
            "source": "binance",
            "batch_id": batch_id,
            "ingested_at": ingested_at
            }
    return record

def validate_kline(record):
    # Check high
    if not (record['high']>=record['open'] and record['high']>=record['close'] and record['high']>=record['low']):
        return False,"High is not the Highest price"
    # Check low
    if not (record['low']<=record['open'] and record['low']<=record['close'] and record['low']<=record['high']):
        return False, "Low is not the lowest price"
    # Check volume
    if record['volume'] <0:
        return False,"Volume can't be Negative"
    # Check prices
    if not (record['open']>0 and record['high']>0 and record['low'] >0 and record['close']>0):
            return False, "Prices must be greater than zero"
    # Check close_time is after open_time
    if record['close_time'] <= record['open_time']:
        return False, "close_time is not after open_time"
    # If everything is valid
    return True, None

#checking and sorting candle data, if good, in clean else in quarantined(error ones)
def transform_and_validate(symbol,raw_klines,interval,batch_id,ingested_at):
    clean =[]
    quarantined=[]
    for raw_candle in raw_klines:
        try:
            record=transform_kline(symbol,interval,raw_candle,batch_id,ingested_at)
            valid, reason=validate_kline(record)
            if valid:
                clean.append(record)
            else:
                quarantined.append({"record": record, "reason": reason})
        except Exception as e:
            quarantined.append({
            "record": raw_candle,  # No valid record due to failure
            "reason": f"TRANSFORMATION_ERROR: {str(e)}"})

    return clean, quarantined


#checking duplicate
def validate_duplicates(records):
    seen = set()
    duplicates = []

    for record in records:
        key = (
            record["symbol"],
            record["interval"],
            record["open_time"]
        )

        if key in seen:
            duplicates.append({
                "type": "duplicate",
                "symbol": record["symbol"],
                "interval": record["interval"],
                "timestamp": record["open_time"],
                "record": record
            })
        else:
            seen.add(key)

    return duplicates

#time into second
def interval_to_seconds(interval):
    unit=interval[-1]
    value=int(interval[:-1])

    multipliers={
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60
    }
    if unit not in multipliers:
        raise ValueError(f"Unsupported interval: {interval}")

    return value * multipliers[unit]

#Seq validating
def validate_sequence(records):
    issues = []

    records_by_key = defaultdict(list)

    for record in records:
        key = (
            record["symbol"],
            record["interval"]
        )

        records_by_key[key].append(record)

    for (symbol, interval), symbol_records in records_by_key.items():

        expected_interval = timedelta(
            seconds=interval_to_seconds(interval)
        )

        symbol_records.sort(
            key=lambda record: record["open_time"]
        )

        for previous, current in zip(
            symbol_records,
            symbol_records[1:]
        ):

            delta = (
                current["open_time"]
                - previous["open_time"]
            )

            if delta > expected_interval:

                missing_candles = (
                    delta // expected_interval
                ) - 1

                issues.append({
                    "type": "gap",
                    "symbol": symbol,
                    "interval": interval,
                    "previous_timestamp": previous["open_time"],
                    "current_timestamp": current["open_time"],
                    "missing_candles": missing_candles
                })

    return issues

##check the duplicate/failuer seq. timestamp issues., 
#if we are not using validateing and seq funciton then use this
#def vealidate_timestamp(records,interval_seconds=60):
    
    sorted_record=sorted(records,
                        key=lambda record:record["open_time"])

    issues=[]

    for i in range(1, len(sorted_record)):
        # Get previous record
        previous_record = sorted_record[i - 1]
        # Get current record
        current_record = sorted_record[i]
         # Extract previous open_time
        previous_timestamp = previous_record["open_time"]
        # Extract current open_time
        current_timestamp = current_record["open_time"]
        timedelta=(current_timestamp-previous_timestamp).total_seconds()
        print(timedelta)
        logging.info(...)
        logging.warning(...)
        logging.error(...)
        
        if timedelta == interval_seconds:
            valid=True
        elif timedelta==0: #duplicate
            issues.append({"type": "duplicate","timestamp": current_timestamp})
        elif timedelta >interval_seconds:#gap
            missing_candles = int(timedelta / interval_seconds - 1)
            issues.append({"type": "gap","missing_candles": missing_candles,
                        "previous_timestamp":previous_timestamp,"current_timestamp":current_timestamp})
        elif timedelta <0: #if not sorted correcttly
            issues.append({"type": "time delta is negative, not sorted properly"})

    return issues

