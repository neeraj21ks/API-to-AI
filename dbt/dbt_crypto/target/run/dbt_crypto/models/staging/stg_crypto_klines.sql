
  create view "neondb"."analytics"."stg_crypto_klines__dbt_tmp"
    
    
  as (
    SELECT
    symbol,
    interval,
    open_time,
    close_time,
    open,
    high,
    low,
    close,
    volume,
    source,
    batch_id,
    ingested_at

FROM public.clean_events
  );