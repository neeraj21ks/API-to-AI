
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT
    symbol,
    interval,
    open_time,
    open,
    high,
    close

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE high < close
  
  
      
    ) dbt_internal_test