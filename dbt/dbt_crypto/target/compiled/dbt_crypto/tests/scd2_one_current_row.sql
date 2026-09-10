SELECT
    symbol
FROM "neondb"."analytics"."dim_symbol_scd2"
GROUP BY symbol
HAVING COUNT(*) FILTER (
    WHERE effective_to IS NULL
) != 1