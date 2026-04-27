with source as (
    select * from {{ source('bot_exchange', 'daily_rates') }}
),

renamed as (
    select
        -- cast DATETIME → DATE, we only need the date part
        cast(period as date)              as rate_date

        -- already well-named, keep as-is
        ,currency_code
        ,currency_name

        -- already FLOAT64, just rename for clarity
        ,buying_sight                      as buying_sight_rate
        ,buying_transfer                   as buying_transfer_rate
        ,selling                           as selling_rate

        -- API-computed values, prefix to distinguish from our own later
        ,mid_rate                          as api_mid_rate
        ,spread_pct                        as api_spread_pct

    from source
)

select * from renamed