import requests
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from urllib3.util.retry import Retry

#this is my primary API, for Failur I can use Fall back API, keep Pipeline up

try: response = requests.get("https://api.binance.com/api/v3/klines",
                        timeout=(3,4))
except Timeout:
    print("The request timed out")
else:
    print("The request did not time out")

#if request not completed, retry procedure

retry_strategy = Retry(
    total=2,
    status_forcelist=[429, 500, 502, 503, 504]
)
github_adapter = HTTPAdapter(max_retries=retry_strategy)

with requests.Session() as session:
    session.mount("https://api.binance.com/api/v3/pklines", github_adapter)
    try:
        response = session.get("https://api.binance.com/api/v3/klines")
    except RetryError as err:
        print(f"Error: {err}")

