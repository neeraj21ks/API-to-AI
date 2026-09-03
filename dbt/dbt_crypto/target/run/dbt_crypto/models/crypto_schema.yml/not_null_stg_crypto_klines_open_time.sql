
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select open_time
from "neondb"."analytics"."stg_crypto_klines"
where open_time is null



  
  
      
    ) dbt_internal_test