
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select trading_date
from "neondb"."analytics"."fct_asset_daily_analytics"
where trading_date is null



  
  
      
    ) dbt_internal_test