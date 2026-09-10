WITH ordered_versions AS (

    SELECT
        symbol,
        effective_from,
        effective_to,

        LEAD(effective_from) OVER (
            PARTITION BY symbol
            ORDER BY effective_from
        ) AS next_effective_from

    FROM "neondb"."analytics"."dim_symbol_scd2"

)

SELECT
    symbol,
    effective_from,
    effective_to,
    next_effective_from

FROM ordered_versions

WHERE effective_to IS NOT NULL
  AND effective_to > next_effective_from