# MTG Scraper 🃏

A professional-grade CLI tool for collecting Magic: The Gathering card prices. Features **eBay API integration** (recommended), **advanced web scraping** with CAPTCHA solving and proxy rotation, and a beautiful interactive menu interface.

**💡 Recommended:** Use **Playwright (option 1)** for scraping that works, with adaptive structure analysis. For production systems, use the **eBay API (option 2)** for legal, reliable data. Scrapy (option 3) demonstrates ethical scraping but is blocked by robots.txt.

```
    __  _____________   _____                                
   /  |/  /_  __/ __ \ / ___/______________ _____  ___  _____
  / /|_/ / / / / / / / \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 / /  / / / / / /_/ / ___/ / /__/ /  / /_/ / /_/ /  __/ /    
/_/  /_/ /_/  \____/ /____/\___/_/   \__,_/ .___/\___/_/     
                                         /_/                 
```

## Features

- 🎮 **Interactive Menu**: Beautiful, easy-to-use menu interface
- 🌐 **Playwright Integration**: Browser automation that works on eBay!
- 🤖 **Adaptive Analyzer**: Auto-discovers page structure & selectors
- 🔍 **Flexible Search**: Search by card name, set, type, or custom query
- 🎯 **API Integration**: eBay Finding API support (official, legal)
- 🕷️ **Scrapy Framework**: Production-grade spider with advanced features
- 🔐 **CAPTCHA Solving**: Dual-mode (2Captcha API + local ML with TensorFlow)
- 🌍 **Proxy Rotation**: Built-in middleware for rotating IP addresses
- 🗄️ **Database Storage**: SQLite integration with SQLAlchemy ORM
- 📊 **Data Visualization**: Beautiful formatted tables with filtering
- 🎨 **Beautiful CLI**: Colorful ASCII art with styled menus
- 📸 **Debug Mode**: Auto-screenshots and visible browser option
- 🔧 **Configurable**: Easy configuration for CAPTCHA, proxies, and APIs

## Data Collection Methods

### 1️⃣ Playwright (Default - Works!)
- **Browser Automation** with real Chrome
  - ✅ **Actually gets results from eBay**
  - 🤖 Adaptive structure analyzer (auto-discovers selectors)
  - ✅ Bypasses robots.txt (acts like real user)
  - ✅ Handles JavaScript automatically  
  - ✅ Stealth mode - harder to detect
  - 🎥 Can run in visible mode to watch it work
  - 📸 Auto-screenshots for debugging
  - 🔍 **Multiple search types:** Card name, set, type, custom
  - Slower but more effective than Scrapy

### 2️⃣ Official API (Best for Production)
- **eBay Finding API**
  - Free API key from [eBay Developers Program](https://developer.ebay.com/)
  - No blocking, clean JSON responses
  - **The legal & professional approach**
  - 🔍 **Multiple search types:** Card name, set, type, custom

### 3️⃣ Scrapy Spider (Educational)
- **Traditional HTTP Scraping**
  - ⚡ Very fast (no browser overhead)
  - 🔧 Production features: CAPTCHA solving, proxies, AutoThrottle
  - ❌ Blocked by eBay's robots.txt (returns 0 results)
  - 📚 Demonstrates ethical scraping & Scrapy expertise

**Recommendation:** Use Playwright (option 1) for actual scraping, or API (option 2) for production.
  
### 🚧 Future Sources
- TCGPlayer API
- CardKingdom integration
- StarCityGames
- Card Market (Europe)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- macOS, Linux, or Windows

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd scraperTool
```

2. **Quick Setup (macOS/Linux):**
```bash
./setup.sh
```

   **Manual Setup:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate

# Install core dependencies (fast)
pip install -r requirements-minimal.txt

# OR install full features (includes TensorFlow - large download)
pip install -r requirements.txt
```

**Note:** TensorFlow is ~500MB. Use `requirements-minimal.txt` if you don't need local ML CAPTCHA solving.

3. (Optional) If using Scrapy-Splash for JavaScript rendering:
```bash
docker run -p 8050:8050 scrapinghub/splash
```

**Note:** Always activate the virtual environment (`source venv/bin/activate`) before running the scraper!

### Configuration (Optional Services)

**1. eBay API (Recommended for production):**
```bash
# Register at https://developer.ebay.com/
export EBAY_API_KEY="your-app-id-here"
```

**2. CAPTCHA Solver (Optional - Choose one):**

Option A - 2Captcha (Paid, Reliable):
```bash
# Install: pip install 2captcha-python
# Register at https://2captcha.com/ (~$3 per 1000 solves)
export CAPTCHA_API_KEY="your-2captcha-api-key"
```

Option B - Local ML Solver (Free, Experimental):
```bash
# Install: pip install tensorflow opencv-python pillow (large download ~500MB)
# Enable local ML solver
export USE_LOCAL_CAPTCHA=true
```

**Tip:** Both are optional! The scraper works without CAPTCHA solving.

**3. Rotating Proxies (For large-scale scraping):**
```bash
# Create proxies.txt with format: http://user:pass@host:port
export PROXY_LIST="proxies.txt"
```

**Make persistent:**
```bash
echo 'export EBAY_API_KEY="your-key"' >> ~/.zshrc
echo 'export CAPTCHA_API_KEY="your-key"' >> ~/.zshrc
```

Use **option 6** in the menu to check configuration status!

## Usage

### Interactive Menu (Recommended)

Simply run the script to launch the beautiful interactive menu:

```bash
python mtgscraper.py
```

The menu provides:
- **1. Playwright Scraper** - Browser automation (With adaptive structure analyzer)
- **2. eBay API Search** - Official API
- **3. Scrapy Spider** - Fast HTTP scraper (demonstrates Scrapy expertise, blocked by robots.txt)
- **4. View Results** - Browse collected data in formatted tables
- **5. View Card Details** - See detailed information for specific cards
- **6. Database Statistics** - View stats about your collection
- **7. Configure Settings** - Set up CAPTCHA, proxies, and API keys
- **8. Clear Database** - Remove all data (with confirmation)
- **0. Exit** - Quit the program

**🎯 Which to Use:**
- **Default/Works:** Option 1 (Playwright - gets real data!)
- **Production/Legal:** Option 2 (eBay API)
- **Learning Scrapy:** Option 3 (Scrapy)

### Direct Command Mode

You can also use the tool directly from command line for scripting:

```bash
# Quick scrape without menu
python mtgscraper.py --card "Black Lotus" --pages 5

# Or with short flags
python mtgscraper.py -c "Lightning Bolt" -p 3
```

### Example Workflows

#### Method 1: eBay API (Recommended)

1. **Get your API key:**
   ```bash
   # Register at developer.ebay.com
   export EBAY_API_KEY="your-app-id"
   ```

2. **Run and search:**
   ```bash
   python mtgscraper.py
   # Select option 1
   # Enter card name
   # View results with option 3
   ```

#### Method 1: Playwright Browser Scraping (Recommended!)

1. **Install Playwright:**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Run and scrape:**
   ```bash
   python mtgscraper.py
   # Select option 1 - Playwright (default!)
   # Choose search type (card name, set, type, custom)
   # Enter your search query
   # Choose headless or visible mode
   # Watch the adaptive analyzer discover page structure!
   # Get actual eBay results! 🎉
   ```

**Search Examples:**
- **By card:** "Black Lotus", "Lightning Bolt"
- **By set:** "Alpha", "Beta", "Modern Masters"  
- **By type:** "creature", "planeswalker", "instant"
- **Custom:** "foil rare mythic"

#### Method 2: eBay API (Production)

1. **Get API key and run:**
   ```bash
   export EBAY_API_KEY="your-app-id"
   python mtgscraper.py
   # Select option 2 - eBay API
   # Choose search type
   # Get official data
   ```

#### Method 3: Scrapy Spider (Educational)

Shows ethical scraping with Scrapy, but blocked by robots.txt:
```bash
# Select option 3
# Gets 0 results (respects robots.txt)
# Demonstrates production Scrapy architecture
```

#### Quick Start (No Configuration)

```bash
python mtgscraper.py
# Select option 1 (API simulated mode available)
# Or select option 2 (basic scraping without CAPTCHA solver)
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--menu` | - | Use interactive menu | True |
| `--card` | `-c` | Card name for direct scraping | - |
| `--pages` | `-p` | Number of pages to scrape | 3 |

**Examples:**
```bash
# Interactive menu (default)
python mtgscraper.py

# Direct scrape
python mtgscraper.py -c "Force of Will" -p 5

# Skip menu
python mtgscraper.py --no-menu -c "Lightning Bolt"
```

## Project Structure

```
scraperTool/
├── mtgscraper/
│   ├── __init__.py          # Package initialization
│   ├── settings.py          # Scrapy settings (AutoThrottle, robots.txt)
│   ├── items.py             # Data models for scraped items
│   ├── pipelines.py         # Database pipeline with SQLAlchemy
│   ├── middlewares.py       # CAPTCHA solver & proxy rotation
│   └── spiders/
│       ├── __init__.py      # Spiders package initialization
│       └── ebay_spider.py   # eBay scraping spider
├── mtgscraper.py            # Main CLI entry point (interactive menu)
├── scrapy.cfg               # Scrapy project configuration
├── requirements.txt         # Python dependencies
├── setup.sh                 # Quick setup script
└── README.md                # This file
```

## Technical Details

### Technologies Used

- **Playwright**: Modern browser automation framework (headless Chrome/Firefox)
- **Scrapy**: High-performance web scraping framework
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Click**: Command-line interface creation framework
- **Colorama**: Cross-platform colored terminal text
- **Tabulate**: Pretty-print tabular data
- **PyFiglet**: ASCII art text generation
- **BeautifulSoup4**: HTML parsing library
- **2Captcha-Python**: Commercial CAPTCHA solving API client
- **TensorFlow**: ML framework for local CAPTCHA solving (optional)
- **OpenCV**: Computer vision library for image processing (optional)
- **Scrapy-Splash**: JavaScript rendering support (optional)

### Database Schema

The SQLite database (`mtg_cards.db`) contains a single table with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| card_name | String | Name of the card |
| set_name | String | Set/edition name |
| price | String | Listed price |
| condition | String | Card condition |
| seller | String | Seller information |
| url | String | Link to listing |
| source | String | Source site (e.g., "eBay") |
| timestamp | String | Scrape timestamp |
| shipping | String | Shipping information |
| buy_it_now | Boolean | Buy It Now listing flag |

### Scrapy Configuration

The scraper is configured with **ethical best practices**:

- **User Agent**: Modern Chrome browser user agent (looks like real user)
- **Download Delay**: 2 seconds between requests (randomized)
- **AutoThrottle**: Automatically adjusts speed based on server load
- **Concurrent Requests**: Limited to 2 per domain (respectful)
- **Robots.txt**: **Enabled** - respects website policies
- **Cookies**: Enabled for session management
- **Retry Logic**: Smart retry with backoff for temporary failures

**Why These Settings Matter:**
- Mimics human browsing behavior
- Reduces server load
- Less likely to be blocked
- Ethical and professional approach
- Shows understanding of web scraping best practices

These settings can be customized in `mtgscraper/settings.py`.

## Development

### Adding a New Source

To add a new scraping source:

1. Create a new spider in `mtgscraper/spiders/`:
```python
# mtgscraper/spiders/tcgplayer_spider.py
import scrapy
from mtgscraper.items import MtgCardItem

class TcgplayerMtgSpider(scrapy.Spider):
    name = 'tcgplayer'
    allowed_domains = ['tcgplayer.com']
    
    def start_requests(self):
        # Your scraping logic here
        pass
    
    def parse(self, response):
        # Your parsing logic here
        pass
```

2. Update the CLI in `mtgscraper.py` to include the new source:
```python
@click.option('--source', '-s', default='ebay', 
              type=click.Choice(['ebay', 'tcgplayer']), 
              help='Source to scrape from')
```

3. Add source-specific configuration to `mtgscraper/settings.py` if needed.

### Customizing Output

To modify the output format, edit the `view` command in `mtgscraper.py`. The `tabulate` library supports multiple table formats:

```python
print(tabulate(rows, headers=headers, tablefmt='fancy_grid'))
# Other formats: 'grid', 'simple', 'plain', 'html', 'latex', etc.
```

## Best Practices & Ethical Scraping

This tool is built with ethical scraping principles in mind:

### 🤖 "Good Bot" Behavior
- **Respect robots.txt**: Always obey website rules (ROBOTSTXT_OBEY = True)
- **Use realistic User-Agents**: Identify as a real browser, not as a bot
- **Control crawl rate**: AutoThrottle adjusts speed based on server capacity
- **Limit concurrency**: Only 2 requests per domain at a time
- **Randomized delays**: Mimic human browsing patterns

### 📋 Interview Talking Points
When discussing this project in interviews, emphasize:

1. **Production-Ready**: "This isn't a toy project - it includes CAPTCHA solving, proxy rotation, and API integration that production systems actually use."

2. **API-First Philosophy**: "I implemented eBay's official API as the primary method because it's legal, reliable, and provides structured data. The scraper is for when APIs aren't available."

3. **Multiple Scraping Approaches**: "I implemented three methods: eBay API for production, Playwright for browser automation that bypasses bot detection, and Scrapy for high-performance HTTP scraping with custom middleware. I understand the trade-offs: Playwright is slower but more effective, Scrapy is faster but easier to block."

4. **Ethical & Legal**: "I respect robots.txt, use AutoThrottle to adapt to server load, and prefer APIs over scraping. This shows professional judgment."

5. **Full-Stack Skills**: "This demonstrates REST APIs, web scraping, middleware development, database design, CLI interfaces, and third-party service integration."

6. **Real-World Challenges**: "I understand anti-bot measures and have solutions: CAPTCHA solvers, proxies, rate limiting. Not just the theory - actual implementations."

### 🚀 Production Features (Already Implemented!)
This scraper includes production-ready features:
- ✅ **CAPTCHA Solving**: 2Captcha integration (configure with API key)
- ✅ **Proxy Rotation**: Built-in middleware for rotating proxies
- ✅ **AutoThrottle**: Adapts crawling speed to server load
- ✅ **Smart Retries**: Exponential backoff for failed requests
- ✅ **API Support**: Official eBay API integration
- ✅ **Configuration Manager**: Easy setup through menu option 6

### 🔮 Future Enhancements
- Distributed crawling with Scrapy Cloud
- More CAPTCHA types (hCaptcha, FunCaptcha)
- User-Agent rotation middleware
- Redis-based job queue
- Monitoring dashboard

## Troubleshooting

### Common Issues

**eBay Scraping Blocked / robots.txt**
- **This is expected!** eBay blocks scraping via robots.txt
- **Why?** Because they provide an official API (the correct approach)
- **Solution**: Use **option 1 (eBay API)** for legal, reliable data access
- **Interview Context**: This demonstrates:
  - Respecting robots.txt (ROBOTSTXT_OBEY = True)
  - Understanding when to use APIs vs. scraping
  - Legal and ethical data collection practices
  - Professional judgment in choosing data sources
- **The scraper respects robots.txt** - showing ethical development practices

**CAPTCHA Challenges**
- **Option 1 (Recommended):** Use 2Captcha API (~$3 per 1000 solves)
  - `export CAPTCHA_API_KEY="your-key"`
- **Option 2 (Free):** Enable local ML solver (experimental)
  - `export USE_LOCAL_CAPTCHA=true`
  - Uses TensorFlow + OpenCV
  - Less reliable than paid service but free
- The middleware automatically tries both methods with fallback

**Import Error: No module named 'mtgscraper'**
- Make sure you're running the script from the project root directory
- Ensure the virtual environment is activated: `source venv/bin/activate`

**Database Not Found**
- Run a scrape first using option 1 in the menu
- The database is created automatically on first scrape

**No Results Found**
- Try a more generic card name (e.g., "Bolt" instead of "Lightning Bolt Alpha Edition")
- Increase the number of pages to scrape
- Check if eBay is blocking (see above)

**Scrapy Deprecation Warnings**
- Warnings about `process_start_requests()` and Splash middleware are normal
- These are from scrapy-splash package compatibility with Scrapy 2.13+
- The code works correctly despite the warnings
- Can be safely ignored - they're about future Scrapy versions

**Twisted Reactor Issues**
- Fixed by using subprocess to run Scrapy
- This allows multiple scrapes in one session
- The interactive menu now works smoothly for repeated scrapes

## Future Enhancements

### Additional Sources
- [ ] TCGPlayer spider
- [ ] CardKingdom spider
- [ ] StarCityGames spider
- [ ] Card Market (Europe)

### Features
- [ ] Export to CSV/JSON
- [ ] Price history tracking over time
- [ ] Price alerts via email/SMS
- [ ] Card comparison tool
- [ ] Market analysis and statistics
- [ ] Web dashboard interface (Flask/Django)

### Production Scaling
- [ ] Rotating proxy middleware
- [ ] User-Agent rotation middleware
- [ ] CAPTCHA solving integration
- [ ] Distributed crawling with Scrapy Cloud
- [ ] Redis-based task queue
- [ ] Monitoring and alerting (Prometheus/Grafana)

## License

This project is provided as-is for educational and portfolio purposes.

## Contributing

This is a portfolio project, but suggestions and improvements are welcome!

---

**Note**: This tool is designed for educational purposes and personal use. Always respect website terms of service and robots.txt files when scraping. Be responsible and ethical in your data collection practices.

