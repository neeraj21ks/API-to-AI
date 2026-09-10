WITH current_symbols AS (

    SELECT
        symbol,
        base_asset,
        quote_asset,
        dbt_valid_from,
        dbt_valid_to

    FROM {{ ref('dim_symbol_snapshot') }}

    WHERE dbt_valid_to IS NULL

)

SELECT
    ROW_NUMBER() OVER (ORDER BY symbol) AS symbol_key,
    symbol,
    base_asset,
    quote_asset,
    dbt_valid_from AS effective_from,
    dbt_valid_to AS effective_to

FROM current_symbols