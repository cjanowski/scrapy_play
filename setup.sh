#!/bin/bash

# MTG Scraper Setup Script

echo "🃏 MTG Scraper - Setup Script"
echo "=============================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip

echo ""
echo "Choose installation type:"
echo "1) Minimal (fast, ~50MB) - Core features only"
echo "2) Full (slow, ~550MB) - Includes TensorFlow for ML CAPTCHA solving"
read -p "Enter choice [1]: " install_choice
install_choice=${install_choice:-1}

if [ "$install_choice" = "2" ]; then
    echo "Installing full dependencies (this may take a while)..."
    pip install -r requirements.txt
else
    echo "Installing minimal dependencies..."
    pip install -r requirements-minimal.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the scraper, run:"
echo "  source venv/bin/activate"
echo "  python mtgscraper.py scrape --card \"Black Lotus\""
echo ""

