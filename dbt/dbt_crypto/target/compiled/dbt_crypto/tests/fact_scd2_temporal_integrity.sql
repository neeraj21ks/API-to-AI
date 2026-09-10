WITH fact_rows AS (

    SELECT
        symbol,
        first_candle_time

    FROM "neondb"."analytics"."fct_asset_daily_analytics"

),

dimension_matches AS (

    SELECT
        f.symbol,
        f.first_candle_time,
        COUNT(d.symbol_key) AS matching_dimension_rows

    FROM fact_rows f

    LEFT JOIN "neondb"."analytics"."dim_symbol_scd2" d
        ON f.symbol = d.symbol
        AND f.first_candle_time >= d.effective_from
        AND (
            f.first_candle_time < d.effective_to
            OR d.effective_to IS NULL
        )

    GROUP BY
        f.symbol,
        f.first_candle_time

)

SELECT *

FROM dimension_matches

WHERE matching_dimension_rows != 1