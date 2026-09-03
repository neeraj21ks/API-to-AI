
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select volume
from "neondb"."analytics"."stg_crypto_klines"
where volume is null



  
  
      
    ) dbt_internal_test