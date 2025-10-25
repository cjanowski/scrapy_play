# dbt Analytics for MTG Scraper

This project includes dbt (data build tool) for transforming and analyzing your scraped MTG card data.

## What is dbt?

dbt is a transformation tool that allows you to write SQL queries to transform your raw scraped data into analytics-ready tables. It provides:

- **Data modeling** - Transform raw data into business-friendly tables
- **Testing** - Ensure data quality with automated tests
- **Documentation** - Auto-generated docs for your data models
- **Version control** - Track changes to your analytics logic

## Installation

```bash
pip install dbt-core dbt-sqlite
```

## Quick Start

### 1. Run a Scrape First

Make sure you have data in your database:
```bash
python mtgscraper.py
# Select option 1 (Playwright Scraper) and scrape some cards
```

### 2. Run dbt Models

From the main menu, select **option 7** (Run dbt Models) or run:
```bash
dbt run --profiles-dir .
```

This creates the following analytics tables:
- `card_price_stats` - Price statistics by card (min, max, avg, median)
- `price_trends` - Price changes over time
- `top_cards` - Top cards ranked by various metrics

### 3. View Analytics

From the main menu, select **option 9** (View Analytics Results)

Or query directly:
```bash
sqlite3 mtg_cards.db "SELECT * FROM top_cards LIMIT 10"
```

## dbt Models Structure

```
models/
├── staging/
│   └── stg_mtg_cards.sql          # Clean raw data
├── marts/
│   ├── core/
│   │   ├── dim_cards.sql          # Card dimension table
│   │   └── fct_card_prices.sql    # Price fact table
│   └── analytics/
│       ├── card_price_stats.sql   # Price statistics
│       ├── price_trends.sql       # Price trends over time
│       └── top_cards.sql          # Top cards by metrics
```

## Available Analytics

### Card Price Statistics

Shows price statistics for each card:
- Listing count
- Min/max/average prices
- Median price
- Price spread
- Buy It Now vs Auction breakdown

```sql
SELECT * FROM card_price_stats ORDER BY avg_price DESC LIMIT 10;
```

### Price Trends

Track how card prices change over time:
- Daily average prices
- Day-over-day price changes
- Percent change

```sql
SELECT * FROM price_trends 
WHERE card_name LIKE '%Black Lotus%' 
ORDER BY scraped_date DESC;
```

### Top Cards

Cards ranked by a "hotness" score (price × log(volume)):
- Highest average price
- Most listings
- Biggest price spreads

```sql
SELECT * FROM top_cards ORDER BY hotness_score DESC LIMIT 20;
```

## Running dbt Commands

All dbt commands should be run with `--profiles-dir .` since we keep the profiles.yml in the project root:

```bash
# Run all models
dbt run --profiles-dir .

# Run specific model
dbt run --select card_price_stats --profiles-dir .

# Run tests
dbt test --profiles-dir .

# Generate and serve documentation
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir . --port 8080
```

## Data Quality Tests

dbt includes automated tests to ensure data quality:

- **Uniqueness tests** - Ensure IDs are unique
- **Not null tests** - Ensure required fields have values
- **Range tests** - Ensure prices are reasonable

Run tests from menu option 8 or:
```bash
dbt test --profiles-dir .
```

## Documentation

Generate interactive documentation:

From menu option 10 or:
```bash
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir . --port 8080
```

This opens a browser with:
- Data lineage graphs
- Column descriptions
- Model documentation
- Test results

## Customizing Models

All models are in the `models/` directory as `.sql` files. You can:

1. Edit existing models to change logic
2. Add new models for custom analytics
3. Update `schema.yml` files to add descriptions and tests

Example: Create a custom model `models/marts/analytics/my_analysis.sql`:

```sql
{{
  config(
    materialized='table',
    tags=['analytics', 'custom']
  )
}}

SELECT
    card_name,
    avg(price_numeric) as avg_price,
    count(*) as total_listings
FROM {{ ref('fct_card_prices') }}
WHERE condition LIKE '%Near Mint%'
GROUP BY card_name
ORDER BY avg_price DESC
```

Then run:
```bash
dbt run --select my_analysis --profiles-dir .
```

## Incremental Processing

By default, models rebuild completely each run. For large datasets, you can use incremental models that only process new data.

## Troubleshooting

### "dbt command not found"
```bash
pip install dbt-core dbt-sqlite
```

### "No such table: mtg_cards"
Run a scrape first to populate the database.

### "Compilation Error"
Check your SQL syntax in the model files. dbt uses Jinja templating.

### Models not showing up
Make sure you ran `dbt run --profiles-dir .` successfully.

## Advanced Usage

### Scheduling dbt with Cron

Add to your cron scraping jobs:
```bash
# After scraping, run dbt to update analytics
0 */6 * * * cd /path/to/scraperTool && dbt run --profiles-dir . >> dbt_cron.log 2>&1
```

### Exporting Analytics

```bash
# Export to CSV
sqlite3 -header -csv mtg_cards.db "SELECT * FROM top_cards;" > top_cards.csv

# Or use the built-in Export function (menu option 11)
```

## Next Steps

1. **Add more models** - Create custom analytics for your needs
2. **Add more tests** - Ensure data quality
3. **Schedule updates** - Automate dbt runs after scraping
4. **Share insights** - Export and share your analytics

## Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [SQL Reference](https://www.sqlite.org/lang.html)
