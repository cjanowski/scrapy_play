{{
  config(
    materialized='table',
    tags=['analytics', 'trends']
  )
}}

-- Analytics: Price trends over time by card and date
select
    card_name,
    set_name,
    scraped_date,
    
    count(*) as daily_listing_count,
    min(price_numeric) as daily_min_price,
    max(price_numeric) as daily_max_price,
    avg(price_numeric) as daily_avg_price,
    
    -- Calculate day-over-day change
    avg(price_numeric) - lag(avg(price_numeric)) over (
        partition by card_name, set_name 
        order by scraped_date
    ) as price_change_from_prev_day,
    
    -- Percent change
    round(
        (avg(price_numeric) - lag(avg(price_numeric)) over (
            partition by card_name, set_name 
            order by scraped_date
        )) / nullif(lag(avg(price_numeric)) over (
            partition by card_name, set_name 
            order by scraped_date
        ), 0) * 100,
        2
    ) as price_change_pct
    
from {{ ref('fct_card_prices') }}
group by card_name, set_name, scraped_date
order by card_name, set_name, scraped_date desc

