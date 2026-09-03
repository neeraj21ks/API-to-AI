
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select candle_count
from "neondb"."analytics"."int_daily_asset_metrics"
where candle_count is null



  
  
      
    ) dbt_internal_test