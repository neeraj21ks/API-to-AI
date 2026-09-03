
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT
    symbol,
    interval,
    open_time,
    close_time

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE close_time < open_time
  
  
      
    ) dbt_internal_test