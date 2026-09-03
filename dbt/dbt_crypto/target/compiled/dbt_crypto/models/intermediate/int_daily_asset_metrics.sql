SELECT
    symbol,
    DATE(open_time) AS trading_date,

    MIN(open_time) AS first_candle_time,
    MAX(open_time) AS last_candle_time,

    (ARRAY_AGG(open ORDER BY open_time))[1] AS daily_open,
    MAX(high) AS daily_high,
    MIN(low) AS daily_low,
    (ARRAY_AGG(close ORDER BY open_time DESC))[1] AS daily_close,

    SUM(volume) AS total_volume,
    COUNT(*) AS candle_count,

    ROUND(
        (
            (
                (ARRAY_AGG(close ORDER BY open_time DESC))[1]
                -
                (ARRAY_AGG(open ORDER BY open_time))[1]
            )
            /
            NULLIF(
                (ARRAY_AGG(open ORDER BY open_time))[1],
                0
            )
        ) * 100,
        4
    ) AS daily_return_pct,

    ROUND(
        (
            (MAX(high) - MIN(low))
            /
            NULLIF(MIN(low), 0)
        ) * 100,
        4
    ) AS daily_range_pct

FROM "neondb"."analytics"."stg_crypto_klines"

GROUP BY
    symbol,
    DATE(open_time)