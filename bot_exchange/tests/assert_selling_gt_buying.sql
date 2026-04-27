-- All exchange rates must be positive numbers.
-- Negative or zero rates would indicate a loading error.
select
    rate_date,
    currency_code,
    buying_sight_rate,
    buying_transfer_rate,
    selling_rate
from {{ ref('fct_exchange_rates') }}
where
    buying_sight_rate     <= 0
    or buying_transfer_rate <= 0
    or selling_rate         <= 0