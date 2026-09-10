
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select effective_from
from "neondb"."analytics"."dim_symbol_scd2"
where effective_from is null



  
  
      
    ) dbt_internal_test