
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT
    symbol
FROM "neondb"."analytics"."dim_symbol_scd2"
GROUP BY symbol
HAVING COUNT(*) FILTER (
    WHERE effective_to IS NULL
) != 1
  
  
      
    ) dbt_internal_test