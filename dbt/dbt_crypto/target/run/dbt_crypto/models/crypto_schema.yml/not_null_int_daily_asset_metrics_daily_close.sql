
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select daily_close
from "neondb"."analytics"."int_daily_asset_metrics"
where daily_close is null



  
  
      
    ) dbt_internal_test