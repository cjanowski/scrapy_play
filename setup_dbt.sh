#!/bin/bash

# Setup script for dbt in MTG Scraper project

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MTG Scraper - dbt Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not detected."
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dbt packages
echo "📦 Installing dbt packages..."
pip install dbt-core dbt-sqlite

# Check if database exists
if [ ! -f "mtg_cards.db" ]; then
    echo ""
    echo "⚠️  No database found (mtg_cards.db)"
    echo "You need to run a scrape first to populate the database."
    echo ""
    echo "Run the scraper:"
    echo "  python mtgscraper.py"
    echo ""
    exit 0
fi

# Run dbt debug to check setup
echo ""
echo "🔍 Checking dbt configuration..."
dbt debug --profiles-dir .

# Ask if user wants to run models now
echo ""
read -p "Run dbt models now? (yes/no): " run_models

if [ "$run_models" = "yes" ]; then
    echo ""
    echo "🚀 Running dbt models..."
    dbt run --profiles-dir .
    
    echo ""
    echo "✅ dbt setup complete!"
    echo ""
    echo "Available analytics tables:"
    echo "  • card_price_stats - Price statistics by card"
    echo "  • price_trends - Price changes over time"
    echo "  • top_cards - Top cards by various metrics"
    echo ""
    echo "View analytics:"
    echo "  python mtgscraper.py"
    echo "  → Select option 9 (View Analytics Results)"
    echo ""
else
    echo ""
    echo "✅ dbt installed successfully!"
    echo ""
    echo "To run dbt models manually:"
    echo "  dbt run --profiles-dir ."
    echo ""
    echo "Or use the interactive menu:"
    echo "  python mtgscraper.py"
    echo "  → Select option 7 (Run dbt Models)"
    echo ""
fi

