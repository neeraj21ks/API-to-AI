
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT
    symbol,
    interval,
    open_time,
    volume

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE volume < 0
  
  
      
    ) dbt_internal_test