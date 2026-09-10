
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select base_asset
from "neondb"."analytics"."dim_symbol_scd2"
where base_asset is null



  
  
      
    ) dbt_internal_test