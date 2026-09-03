
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select open
from "neondb"."analytics"."stg_crypto_klines"
where open is null



  
  
      
    ) dbt_internal_test