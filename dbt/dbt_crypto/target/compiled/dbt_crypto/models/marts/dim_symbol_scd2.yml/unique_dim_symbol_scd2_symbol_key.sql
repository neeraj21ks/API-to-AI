
    
    

select
    symbol_key as unique_field,
    count(*) as n_records

from "neondb"."analytics"."dim_symbol_scd2"
where symbol_key is not null
group by symbol_key
having count(*) > 1


