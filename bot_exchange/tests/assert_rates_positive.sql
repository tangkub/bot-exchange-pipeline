-- Selling rate must always be higher than buying transfer rate.
-- Returns failing rows — test passes only when this returns 0 rows.
select
    rate_date
    ,currency_code
    ,buying_transfer_rate
    ,selling_rate
from {{ ref('fct_exchange_rates') }}
where selling_rate <= buying_transfer_rate