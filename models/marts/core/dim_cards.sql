{{
  config(
    materialized='table',
    tags=['core', 'dimension']
  )
}}

-- Dimension table: Unique cards with their latest information
with latest_cards as (
    select
        card_name,
        set_name,
        max(scraped_at) as latest_scrape
    from {{ ref('stg_mtg_cards') }}
    group by card_name, set_name
),

card_details as (
    select
        s.card_name,
        s.set_name,
        s.condition,
        s.source,
        s.scrape_method,
        s.scraped_at
    from {{ ref('stg_mtg_cards') }} s
    inner join latest_cards l
        on s.card_name = l.card_name
        and s.set_name = l.set_name
        and s.scraped_at = l.latest_scrape
)

select
    row_number() over (order by card_name, set_name) as card_key,
    card_name,
    set_name,
    condition as typical_condition,
    source as latest_source,
    scrape_method,
    scraped_at as last_updated
from card_details

