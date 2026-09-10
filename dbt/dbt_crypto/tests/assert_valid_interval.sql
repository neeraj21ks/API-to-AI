SELECT
    symbol,
    interval,
    open_time

FROM {{ ref('stg_crypto_klines') }}

WHERE interval <> '1m'
