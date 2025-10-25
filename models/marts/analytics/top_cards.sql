{{
  config(
    materialized='table',
    tags=['analytics', 'summary']
  )
}}

-- Analytics: Top cards by various metrics
with card_stats as (
    select * from {{ ref('card_price_stats') }}
),

ranked_cards as (
    select
        card_name,
        set_name,
        avg_price,
        listing_count,
        min_price,
        max_price,
        price_spread,
        
        -- Rank by different metrics
        row_number() over (order by avg_price desc) as rank_by_avg_price,
        row_number() over (order by max_price desc) as rank_by_max_price,
        row_number() over (order by listing_count desc) as rank_by_volume,
        row_number() over (order by price_spread desc) as rank_by_spread
        
    from card_stats
)

select
    card_name,
    set_name,
    round(avg_price, 2) as avg_price,
    listing_count,
    round(min_price, 2) as min_price,
    round(max_price, 2) as max_price,
    round(price_spread, 2) as price_spread,
    rank_by_avg_price,
    rank_by_max_price,
    rank_by_volume,
    rank_by_spread,
    
    -- Overall "hotness" score (combination of price and volume)
    round(avg_price * log(listing_count + 1), 2) as hotness_score
    
from ranked_cards
order by hotness_score desc

