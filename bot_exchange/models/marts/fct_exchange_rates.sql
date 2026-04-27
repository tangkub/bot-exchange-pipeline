{{ config(materialized='table') }}

-- Pull from staging, never from the raw table directly
with staged as (
    select * from {{ ref('stg_exchange_rates') }}
)

select
    -- identifiers
    rate_date
    ,currency_code
    ,currency_name

    -- raw rates (passed through from staging)
    ,buying_sight_rate
    ,buying_transfer_rate
    ,selling_rate

    -- own computed spread: difference between sell and buy
    ,round(selling_rate - buying_transfer_rate, 4)             as spread

    -- own computed mid-rate: average of buy transfer and sell
    ,round((buying_transfer_rate + selling_rate) / 2, 4)       as mid_rate

    -- computed mid_rate vs API mid_rate difference
    ,round(
        abs(((buying_transfer_rate + selling_rate) / 2) - api_mid_rate)
    , 4)                                                        as mid_rate_diff

    -- tolerance flag: 'OK' if diff < 0.01, 'WARN' if < 0.05, 'FAIL' if >= 0.05
    ,case
        when abs(((buying_transfer_rate + selling_rate) / 2) - api_mid_rate) < 0.01
            then 'OK'
        when abs(((buying_transfer_rate + selling_rate) / 2) - api_mid_rate) < 0.05
            then 'WARN'
        else
            'FAIL'
    end                                                         as mid_rate_check

    -- API reference values (kept for auditability)
    ,api_mid_rate
    ,api_spread_pct

    -- date dimensions for easy filtering in Looker Studio
    ,extract(year    from rate_date)                          as year
    ,extract(month   from rate_date)                          as month
    ,extract(quarter from rate_date)                          as quarter
    ,format_date('%Y-%m', rate_date)                          as year_month

from staged