{% snapshot dim_symbol_snapshot %}

{{
    config(
        target_schema='analytics',
        unique_key='symbol',
        strategy='check',
        check_cols=['base_asset', 'quote_asset']
    )
}}

SELECT
    symbol,
    base_asset,
    quote_asset
FROM {{ ref('symbol_metadata') }}

{% endsnapshot %}