import requests
import logging
import uuid

from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.load import load_to_neon, load_raw_event, load_clean_events,create_batch,update_batch_status
from src.kline_process import process_klines

#which symbol data need to fetch
SYMBOLS = ["BTCUSDT","ETHUSDT","SOLUSDT"]

# if fail, Retry procedure
retry_statergy = Retry(total=2, connect=2,status=2,backoff_factor=0.1,
                status_forcelist=[429, 500, 502, 503, 504],allowed_methods={"GET"},raise_on_status=False)

binance_adapter = HTTPAdapter(max_retries=retry_statergy)

session=requests.Session()
session.mount("https://",binance_adapter)

#Log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

#this is my primary API, for Failur I can use Fall back API, keep Pipeline up
def fetch_klines(symbol, interval='1m',limit=10,):
    params={"symbol":symbol,"interval":interval,"limit":limit}
    logger.info(f"Fetching {symbol} from Binance")

    try:
        response = session.get("https://api.binance.com/api/v3/klines",params=params,timeout=10)
        response.raise_for_status()
        data=response.json()
        logger.info(f"{symbol} fetched successfully|"f"Records: {len(data)}")
        return data
    #if first fail, move no next, don't stop after failur attempt all
    except requests.exceptions.RequestException as err:
        logger.error(f"Binance request failed for {symbol} | {err}")
        return None

#orchestration
# orchestration

batch_id = str(uuid.uuid4())
started_at = datetime.now(timezone.utc)
ingested_at = started_at

records_extracted = 0
records_loaded = 0
records_quarantined = 0

logger.info(
    f"Starting pipeline batch | batch_id={batch_id} | ingested_at={ingested_at}"
)

create_batch(
    batch_id=batch_id,
    source="binance",
    started_at=started_at
)

for symbol in SYMBOLS:

    data = fetch_klines(symbol)

    if data is None:
        logger.warning(f"No data received for {symbol}")
        continue

    records_extracted += len(data)

    load_raw_event(
    batch_id=batch_id,
    source="binance",
    symbol=symbol,
    interval="1m",
    payload=data,
    ingested_at=ingested_at
    )

    clean, quarantined = process_klines(
        symbol=symbol,
        raw_klines=data,
        interval="1m",
        batch_id=batch_id,
        ingested_at=ingested_at
    )

    records_loaded += len(clean)
    records_quarantined += len(quarantined)
    load_clean_events(clean)

completed_at = datetime.now(timezone.utc)

update_batch_status(
    batch_id=batch_id,
    status="SUCCESS",
    completed_at=completed_at,
    records_extracted=records_extracted,
    records_loaded=records_loaded,
    records_quarantined=records_quarantined
)

logger.info(
    f"Pipeline batch completed | "
    f"batch_id={batch_id} | "
    f"extracted={records_extracted} | "
    f"loaded={records_loaded} | "
    f"quarantined={records_quarantined}"
)

#testing part
#from transform import transform_and_validate
#record =transform_and_validate("BTCUSDT",data[0])
#print(record)