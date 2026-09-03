WITH daily_metrics AS (

    SELECT *
    FROM {{ ref('int_daily_asset_metrics') }}

),

analytics AS (

    SELECT
        symbol,
        trading_date,
        first_candle_time,
        last_candle_time,
        daily_open,
        daily_high,
        daily_low,
        daily_close,
        total_volume,
        candle_count,
        daily_return_pct,
        daily_range_pct,

        LAG(daily_close) OVER (
            PARTITION BY symbol
            ORDER BY trading_date
        ) AS previous_daily_close,

        RANK() OVER (
            PARTITION BY trading_date
            ORDER BY daily_return_pct DESC
        ) AS performance_rank,

        RANK() OVER (
            PARTITION BY trading_date
            ORDER BY daily_range_pct DESC
        ) AS volatility_rank

    FROM daily_metrics

)

SELECT
    symbol,
    trading_date,
    first_candle_time,
    last_candle_time,
    daily_open,
    daily_high,
    daily_low,
    daily_close,
    total_volume,
    candle_count,
    daily_return_pct,
    daily_range_pct,
    previous_daily_close,

    ROUND(
        (
            (daily_close - previous_daily_close)
            / NULLIF(previous_daily_close, 0)
        ) * 100,
        4
    ) AS day_over_day_return_pct,

    performance_rank,
    volatility_rank

FROM analytics
