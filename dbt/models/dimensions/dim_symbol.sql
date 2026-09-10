SELECT
    ROW_NUMBER() OVER (ORDER BY symbol) AS symbol_key,
    symbol,
    SPLIT_PART(symbol, 'USDT', 1) AS base_asset,
    'USDT' AS quote_asset
FROM (
    SELECT DISTINCT symbol
    FROM {{ ref('stg_crypto_klines') }}
)