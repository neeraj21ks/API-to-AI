
      update "neondb"."analytics"."dim_symbol_snapshot"
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "dim_symbol_snapshot__dbt_tmp000110842943" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = "neondb"."analytics"."dim_symbol_snapshot".dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and "neondb"."analytics"."dim_symbol_snapshot".dbt_valid_to is null;
      


    insert into "neondb"."analytics"."dim_symbol_snapshot" ("symbol", "base_asset", "quote_asset", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."symbol",DBT_INTERNAL_SOURCE."base_asset",DBT_INTERNAL_SOURCE."quote_asset",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "dim_symbol_snapshot__dbt_tmp000110842943" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;

  