
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT
    symbol,
    interval,
    open_time

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE symbol NOT IN ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')
  
  
      
    ) dbt_internal_test