{{
  config(
    materialized='view',
    tags=['staging']
  )
}}

-- Staging model: Clean and standardize raw MTG card data
with source_data as (
    select * from mtg_cards
),

cleaned as (
    select
        id,
        card_name,
        set_name,
        
        -- Clean price: extract numeric value
        -- Convert "$1,234.56" to 1234.56
        replace(replace(replace(price, '$', ''), ',', ''), ' to ', '-') as price_raw,
        
        -- Try to extract first price if range
        cast(
            replace(
                replace(
                    replace(
                        case 
                            when instr(replace(replace(price, '$', ''), ',', ''), ' to ') > 0 
                            then substr(replace(replace(price, '$', ''), ',', ''), 1, instr(replace(replace(price, '$', ''), ',', ''), ' to ') - 1)
                            else replace(replace(price, '$', ''), ',', '')
                        end,
                        '$', ''
                    ),
                    ',', ''
                ),
                ' ', ''
            ) as real
        ) as price_numeric,
        
        condition,
        seller,
        url,
        source,
        
        -- Parse timestamp
        datetime(timestamp) as scraped_at,
        date(timestamp) as scraped_date,
        
        shipping,
        buy_it_now,
        
        -- Extract source type
        case 
            when source like '%API%' then 'API'
            when source like '%Playwright%' then 'Playwright'
            when source like '%Scrapy%' then 'Scrapy'
            else 'Unknown'
        end as scrape_method
        
    from source_data
    where card_name is not null
      and price is not null
)

select * from cleaned

