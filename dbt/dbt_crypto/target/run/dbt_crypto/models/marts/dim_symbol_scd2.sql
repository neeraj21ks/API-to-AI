
  create view "neondb"."analytics"."dim_symbol_scd2__dbt_tmp"
    
    
  as (
    WITH symbol_history AS (

    SELECT
        symbol,
        base_asset,
        quote_asset,
        dbt_scd_id,
        dbt_valid_from,
        dbt_valid_to

    FROM "neondb"."analytics"."dim_symbol_snapshot"

)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY symbol, dbt_valid_from
    ) AS symbol_key,

    symbol,
    base_asset,
    quote_asset,

    dbt_valid_from AS effective_from,
    dbt_valid_to AS effective_to,

    dbt_scd_id

FROM symbol_history
  );