WITH daily_metrics AS (

    SELECT *
    FROM "neondb"."analytics"."int_daily_asset_metrics"

),

symbol_dimension AS (

    SELECT
        symbol_key,
        symbol,
        base_asset,
        quote_asset,
        effective_from,
        effective_to

    FROM "neondb"."analytics"."dim_symbol_scd2"

),

analytics AS (

    SELECT
        d.symbol_key,

        m.symbol,
        m.trading_date,
        m.first_candle_time,
        m.last_candle_time,

        m.daily_open,
        m.daily_high,
        m.daily_low,
        m.daily_close,

        m.total_volume,
        m.candle_count,

        m.daily_return_pct,
        m.daily_range_pct,

        LAG(m.daily_close) OVER (
            PARTITION BY m.symbol
            ORDER BY m.trading_date
        ) AS previous_daily_close,

        RANK() OVER (
            PARTITION BY m.trading_date
            ORDER BY m.daily_return_pct DESC
        ) AS performance_rank,

        RANK() OVER (
            PARTITION BY m.trading_date
            ORDER BY m.daily_range_pct DESC
        ) AS volatility_rank

    FROM daily_metrics m

    INNER JOIN symbol_dimension d
        ON m.symbol = d.symbol

        AND m.first_candle_time >= d.effective_from

        AND (
            m.first_candle_time < d.effective_to
            OR d.effective_to IS NULL
        )

)

SELECT
    symbol_key,
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