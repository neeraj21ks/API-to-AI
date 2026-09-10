
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select symbol_key
from "neondb"."analytics"."dim_symbol_scd2"
where symbol_key is null



  
  
      
    ) dbt_internal_test