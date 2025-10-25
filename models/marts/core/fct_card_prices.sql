{{
  config(
    materialized='table',
    tags=['core', 'fact']
  )
}}

-- Fact table: All card price observations
select
    id as price_id,
    card_name,
    set_name,
    price_numeric,
    price_raw,
    condition,
    seller,
    shipping,
    buy_it_now,
    source,
    scrape_method,
    scraped_at,
    scraped_date,
    url
from {{ ref('stg_mtg_cards') }}
where price_numeric > 0  -- Filter out invalid prices
  and price_numeric < 1000000  -- Filter out unrealistic prices

