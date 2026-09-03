
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select low
from "neondb"."analytics"."stg_crypto_klines"
where low is null



  
  
      
    ) dbt_internal_test