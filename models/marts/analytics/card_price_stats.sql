{{
  config(
    materialized='table',
    tags=['analytics', 'pricing']
  )
}}

-- Analytics: Price statistics by card
select
    card_name,
    set_name,
    
    -- Price statistics
    count(*) as listing_count,
    min(price_numeric) as min_price,
    max(price_numeric) as max_price,
    avg(price_numeric) as avg_price,
    
    -- Buy it now vs auction
    sum(case when buy_it_now then 1 else 0 end) as buy_it_now_count,
    sum(case when not buy_it_now then 1 else 0 end) as auction_count,
    
    -- Average price by type
    avg(case when buy_it_now then price_numeric end) as avg_buy_it_now_price,
    avg(case when not buy_it_now then price_numeric end) as avg_auction_price,
    
    -- Latest scrape info
    max(scraped_at) as last_scraped,
    min(scraped_at) as first_scraped,
    
    -- Price spread
    max(price_numeric) - min(price_numeric) as price_spread,
    (max(price_numeric) - min(price_numeric)) / nullif(avg(price_numeric), 0) * 100 as price_spread_pct
    
from {{ ref('fct_card_prices') }} main
group by card_name, set_name
having count(*) >= 1
order by avg_price desc
