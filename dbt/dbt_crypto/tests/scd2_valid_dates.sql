SELECT *
FROM {{ ref('dim_symbol_scd2') }}
WHERE effective_to IS NOT NULL
  AND effective_to <= effective_from