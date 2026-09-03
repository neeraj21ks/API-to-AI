SELECT
    symbol,
    interval,
    open_time,
    open,
    high,
    low,
    close

FROM {{ ref('fact_crypto_klines') }}

WHERE
       high < open
    OR high < close
    OR high < low
    OR low > open
    OR low > close
    OR low > high
    OR volume < 0