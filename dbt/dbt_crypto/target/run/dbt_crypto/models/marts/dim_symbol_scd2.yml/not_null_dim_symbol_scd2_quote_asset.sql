
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select quote_asset
from "neondb"."analytics"."dim_symbol_scd2"
where quote_asset is null



  
  
      
    ) dbt_internal_test