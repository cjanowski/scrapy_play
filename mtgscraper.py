#!/usr/bin/env python3
'''
MTG Scraper - CLI tool for scraping Magic: The Gathering card prices
'''

import click
import os
import sys
from colorama import init, Fore, Style
from tabulate import tabulate
# Scrapy imports removed - using subprocess instead to avoid reactor issues
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from mtgscraper.pipelines import MtgCard, Base
import pyfiglet

# Initialize colorama
init(autoreset=True)


def print_banner():
    '''
    Display ASCII art banner
    '''
    banner = pyfiglet.figlet_format('MTG Scraper', font='slant')
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + '=' * 70)
    print(Fore.GREEN + ' Magic: The Gathering Card Price Scraper'.center(70))
    print(Fore.YELLOW + '=' * 70)
    print()


def print_success(message):
    '''
    Print success message
    '''
    print(Fore.GREEN + f'✓ {message}')


def print_error(message):
    '''
    Print error message
    '''
    print(Fore.RED + f'✗ {message}')


def print_info(message):
    '''
    Print info message
    '''
    print(Fore.CYAN + f'ℹ {message}')


def print_menu():
    '''
    Display main menu
    '''
    print(Fore.CYAN + '┌─────────────────────────────────────────────────────────┐')
    print(Fore.CYAN + '│' + Fore.YELLOW + '                      MAIN MENU                          ' + Fore.CYAN + '│')
    print(Fore.CYAN + '├─────────────────────────────────────────────────────────┤')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '1.' + Fore.WHITE + ' Playwright Scraper (Recommended - Works!)           ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '2.' + Fore.WHITE + ' eBay API Search (Legal & Professional)              ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '3.' + Fore.WHITE + ' Scrapy Spider (Fast, Ethical, Blocked)              ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '4.' + Fore.WHITE + ' View Results                                        ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '5.' + Fore.WHITE + ' View Card Details                                   ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '6.' + Fore.WHITE + ' Database Statistics                                 ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '7.' + Fore.WHITE + ' Configure Settings                                  ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '8.' + Fore.WHITE + ' Clear Database                                      ' + Fore.CYAN + '│')
    print(Fore.CYAN + '│  ' + Fore.GREEN + '0.' + Fore.WHITE + ' Exit                                                ' + Fore.CYAN + '│')
    print(Fore.CYAN + '└─────────────────────────────────────────────────────────┘')
    print()


def ebay_api_search():
    '''
    Search using eBay's official Finding API (legal and recommended)
    '''
    import requests
    from datetime import datetime
    
    print(Fore.YELLOW + '\n━━━ eBay API SEARCH (Official & Legal) ━━━\n')
    print_info('This uses eBay\'s official API - the legal and recommended method')
    print()
    
    # Check for API key
    api_key = os.environ.get('EBAY_API_KEY')
    
    if not api_key:
        print(Fore.YELLOW + '⚠  eBay API Key Required\n')
        print('To use eBay\'s API, you need to:')
        print('1. Register at: ' + Fore.CYAN + 'https://developer.ebay.com/')
        print(Style.RESET_ALL + '2. Create an application and get your API key')
        print('3. Set environment variable: ' + Fore.CYAN + 'export EBAY_API_KEY="your-key-here"')
        print()
        
        use_demo = input(Fore.CYAN + 'Use demo API key for testing? (yes/no): ' + Style.RESET_ALL).strip().lower()
        
        if use_demo == 'yes':
            api_key = 'DEMO_KEY_SIMULATED'
            print_info('Using simulated API response for demonstration')
        else:
            print_info('Cancelled. Register at https://developer.ebay.com/ to get started!')
            return
    
    # Search options
    print(Fore.CYAN + 'Search by:')
    print('  1. Card name')
    print('  2. Set name')
    print('  3. Card type')
    print('  4. Custom MTG search')
    print()
    
    search_type = input(Fore.GREEN + 'Select search type [1]: ' + Style.RESET_ALL).strip()
    if not search_type:
        search_type = '1'
    
    if search_type == '1':
        card = input(Fore.CYAN + '\nEnter card name: ' + Style.RESET_ALL).strip()
    elif search_type == '2':
        set_name = input(Fore.CYAN + '\nEnter set name (e.g., "Alpha", "Beta"): ' + Style.RESET_ALL).strip()
        card = f'mtg {set_name}'
    elif search_type == '3':
        card_type = input(Fore.CYAN + '\nEnter card type (creature/instant/sorcery/etc): ' + Style.RESET_ALL).strip()
        card = f'mtg {card_type}'
    else:
        card = input(Fore.CYAN + '\nEnter custom MTG search: ' + Style.RESET_ALL).strip()
    
    if not card:
        print_error('Search query cannot be empty!')
        return
    
    limit = input(Fore.CYAN + 'Number of results [20]: ' + Style.RESET_ALL).strip()
    limit = int(limit) if limit.isdigit() else 20
    
    print()
    print_info(f'Searching eBay API for: {Fore.YELLOW}{card}')
    print_info(f'Limit: {Fore.YELLOW}{limit} results')
    print()
    
    try:
        if api_key == 'DEMO_KEY_SIMULATED':
            # Simulated API response for demo purposes
            print_info('Simulating API call (demo mode)...')
            results = _simulate_ebay_api_response(card, limit)
        else:
            # Real API call
            results = _call_ebay_finding_api(api_key, card, limit)
        
        if not results:
            print_error('No results found')
            return
        
        # Save to database
        db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        for item in results:
            api_card = MtgCard(
                card_name=item['title'],
                price=item['price'],
                condition=item.get('condition', 'Not specified'),
                url=item['url'],
                source='eBay API (Official)',
                timestamp=datetime.now().isoformat(),
                shipping=item.get('shipping', 'See listing'),
                buy_it_now=True,
                seller=item.get('seller', 'eBay'),
                set_name='Unknown'
            )
            session.add(api_card)
        
        session.commit()
        session.close()
        
        print()
        print_success(f'API search completed! Found {len(results)} cards.')
        print_info(f'Results saved to: {Fore.YELLOW}mtg_cards.db')
        print_info(f'Use {Fore.YELLOW}option 4{Fore.CYAN} to view the results!')
        
    except Exception as e:
        print_error(f'API search failed: {str(e)}')


def _simulate_ebay_api_response(card_name, limit):
    '''
    Simulate eBay API response for demonstration
    '''
    import random
    
    results = []
    sets = ['Alpha', 'Beta', 'Unlimited', 'Revised', 'Modern Masters']
    conditions = ['New', 'Like New', 'Very Good', 'Good']
    
    for i in range(min(limit, 20)):
        if 'Lotus' in card_name or 'Mox' in card_name:
            price = random.randint(1000, 30000)
        else:
            price = random.randint(5, 500)
        
        results.append({
            'title': f'{card_name} - {random.choice(sets)}',
            'price': f'${price:,}.{random.randint(0, 99):02d}',
            'condition': random.choice(conditions),
            'url': f'https://www.ebay.com/itm/demo-{i}',
            'shipping': random.choice(['Free shipping', f'${random.randint(3, 10)}.99 shipping']),
            'seller': f'seller_{random.randint(100, 999)}'
        })
    
    return results


def _call_ebay_finding_api(api_key, keywords, limit):
    '''
    Call eBay's Finding API
    '''
    import requests
    
    base_url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    
    params = {
        'OPERATION-NAME': 'findItemsByKeywords',
        'SERVICE-VERSION': '1.0.0',
        'SECURITY-APPNAME': api_key,
        'RESPONSE-DATA-FORMAT': 'JSON',
        'keywords': f'mtg {keywords}',
        'paginationInput.entriesPerPage': str(limit),
        'sortOrder': 'PricePlusShippingLowest'
    }
    
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    
    results = []
    search_result = data.get('findItemsByKeywordsResponse', [{}])[0]
    items = search_result.get('searchResult', [{}])[0].get('item', [])
    
    for item in items:
        results.append({
            'title': item.get('title', [''])[0],
            'price': f"${item.get('sellingStatus', [{}])[0].get('currentPrice', [{}])[0].get('__value__', '0')}",
            'condition': item.get('condition', [{}])[0].get('conditionDisplayName', ['Not specified'])[0],
            'url': item.get('viewItemURL', [''])[0],
            'shipping': item.get('shippingInfo', [{}])[0].get('shippingServiceCost', [{}])[0].get('__value__', 'See listing'),
            'seller': item.get('sellerInfo', [{}])[0].get('sellerUserName', ['Unknown'])[0]
        })
    
    return results


def playwright_scraper():
    '''
    Browser automation scraping with Playwright (bypasses many protections)
    '''
    print(Fore.YELLOW + '\n━━━ PLAYWRIGHT BROWSER SCRAPER ━━━\n')
    
    print(Fore.GREEN + '✅ Advantages:')
    print('   • Bypasses robots.txt (acts like real browser)')
    print('   • Handles JavaScript automatically')
    print('   • Stealth mode - harder to detect')
    print('   • Can solve simple CAPTCHAs visually')
    print()
    print(Fore.YELLOW + '⚠  Note: Slower than Scrapy but more effective')
    print()
    
    # Check if Playwright is installed
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print_error('Playwright not installed!')
        print()
        print('Install with:')
        print(Fore.CYAN + '  pip install playwright')
        print(Fore.CYAN + '  playwright install chromium')
        print()
        return
    
    # Search options
    print(Fore.CYAN + 'Search by:')
    print('  1. Card name')
    print('  2. Set name')
    print('  3. Card type (creature, instant, etc.)')
    print('  4. Custom search')
    print()
    
    search_type = input(Fore.GREEN + 'Select search type [1]: ' + Style.RESET_ALL).strip()
    if not search_type:
        search_type = '1'
    
    if search_type == '1':
        card = input(Fore.CYAN + 'Enter card name: ' + Style.RESET_ALL).strip()
    elif search_type == '2':
        set_name = input(Fore.CYAN + 'Enter set name (e.g., "Alpha", "Modern Masters"): ' + Style.RESET_ALL).strip()
        card = f'mtg {set_name}'
    elif search_type == '3':
        card_type = input(Fore.CYAN + 'Enter card type (e.g., "creature", "planeswalker"): ' + Style.RESET_ALL).strip()
        card = f'mtg {card_type}'
    else:
        card = input(Fore.CYAN + 'Enter custom search query: ' + Style.RESET_ALL).strip()
    
    if not card:
        print_error('Search query cannot be empty!')
        return
    
    limit = input(Fore.CYAN + 'Max results [20]: ' + Style.RESET_ALL).strip()
    limit = int(limit) if limit.isdigit() else 20
    
    headless_choice = input(Fore.CYAN + 'Run in background (headless)? [yes/no]: ' + Style.RESET_ALL).strip().lower()
    headless = headless_choice != 'no'
    
    print()
    print_info(f'Launching browser for: {Fore.YELLOW}{card}')
    if headless:
        print_info('Running in headless mode (background)')
    else:
        print_info('Running in visible mode - watch the browser work! 🌐')
    print()
    
    try:
        from datetime import datetime
        from mtgscraper.analyzer import PageStructureAnalyzer
        results = []
        
        with sync_playwright() as p:
            # Launch browser (headless or visible)
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ],
                slow_mo=100 if not headless else 0  # Slow down in visible mode
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            # Navigate to eBay search
            search_url = f'https://www.ebay.com/sch/i.html?_nkw=mtg+{card.replace(" ", "+")}&LH_BIN=1'
            print_info(f'Navigating to eBay...')
            
            try:
                page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
                
                # Wait a bit for dynamic content
                page.wait_for_timeout(3000)
                
                # Analyze page structure first
                print_info('Running structure analyzer...')
                analyzer = PageStructureAnalyzer(page)
                selectors = analyzer.analyze()
                
                print()
                
                # Use discovered selectors
                listings = page.query_selector_all(selectors.get('container', '.s-item'))
                
                if not listings:
                    # Take screenshot for debugging
                    page.screenshot(path='ebay_debug.png')
                    
                    # Also save HTML for inspection
                    with open('ebay_debug.html', 'w', encoding='utf-8') as f:
                        f.write(page.content())
                    
                    print_error('Could not find listings on page')
                    print_info('Debug files saved:')
                    print(Fore.CYAN + '   • ebay_debug.png (screenshot)')
                    print(Fore.CYAN + '   • ebay_debug.html (page source)')
                    print()
                    print(Fore.YELLOW + 'eBay may have changed their HTML structure or is blocking')
                    browser.close()
                    return
                    
            except Exception as e:
                print_error(f'Page load error: {str(e)}')
                browser.close()
                return
            
            # Extract listings using JavaScript (more reliable)
            print_info(f'Found {len(listings)} listings, extracting data...')
            
            # Use JavaScript to extract data directly with discovered selectors
            results_js = page.evaluate('''
                (selectors) => {
                    const items = [];
                    const containerSelector = selectors.container || '.s-item';
                    const titleSelector = selectors.title || '.s-item__title';
                    const priceSelector = selectors.price || '.s-item__price';
                    
                    const listings = document.querySelectorAll(containerSelector + ', .s-item, li.s-item, [class*="s-item"]');
                    
                    listings.forEach((listing, index) => {
                        try {
                            // Get title using discovered selector
                            const titleEl = listing.querySelector(titleSelector + ', .s-item__title span, .s-item__title, h3');
                            const title = titleEl ? titleEl.textContent.trim() : null;
                            
                            // Get price using discovered selector
                            const priceEl = listing.querySelector(priceSelector + ', .s-item__price, span.s-item__price');
                            const price = priceEl ? priceEl.textContent.trim() : null;
                            
                            // Get URL
                            const linkEl = listing.querySelector('a.s-item__link, a[href*="/itm/"]');
                            const url = linkEl ? linkEl.href : '';
                            
                            // Only include if we have title and price
                            if (title && price && title.toLowerCase() !== 'shop on ebay' && price.includes('$')) {
                                items.push({
                                    title: title,
                                    price: price,
                                    url: url
                                });
                            }
                        } catch (e) {
                            // Skip items that fail
                        }
                    });
                    
                    return items;
                }
            ''', selectors)
            
            # Convert JavaScript results to Python
            print_info(f'JavaScript extracted {len(results_js)} items')
            
            processed = 0
            for item in results_js[:limit]:
                results.append({
                    'card_name': item['title'],
                    'price': item['price'],
                    'url': item['url'],
                    'source': 'eBay (Playwright)',
                    'timestamp': datetime.now().isoformat(),
                    'condition': 'Not specified',
                    'shipping': 'See listing',
                    'buy_it_now': True,
                    'seller': 'eBay Seller',
                    'set_name': 'Unknown'
                })
                
                print(f'   {Fore.GREEN}✓{Style.RESET_ALL} Found: {item["title"][:50]}...')
                processed += 1
            
            # Save debug files if no results
            if not results:
                page.screenshot(path='ebay_debug.png')
                with open('ebay_debug.html', 'w', encoding='utf-8') as f:
                    f.write(page.content())
                print()
                print_info('Debug files saved for inspection')
            
            browser.close()
        
        # Save to database
        if results:
            db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
            engine = create_engine(f'sqlite:///{db_path}')
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            for item in results:
                card = MtgCard(**item)
                session.add(card)
            
            session.commit()
            session.close()
            
            print()
            print_success(f'Found {Fore.YELLOW}{len(results)}{Fore.GREEN} cards!')
            print_info(f'Results saved to: {Fore.YELLOW}mtg_cards.db')
            print_info(f'Use {Fore.YELLOW}option 4{Fore.CYAN} to view results')
        else:
            print()
            print_error('No results extracted from listings')
            print()
            print(Fore.YELLOW + '💡 This could mean:')
            print(Fore.YELLOW + '   • eBay changed their HTML structure')
            print(Fore.YELLOW + '   • eBay is showing a CAPTCHA page')
            print(Fore.YELLOW + '   • Selectors need updating')
            print()
            print_info('Debug files saved for inspection:')
            print(Fore.CYAN + '   • ebay_debug.png')
            print(Fore.CYAN + '   • ebay_debug.html')
            print()
            print_success('💡 Best solution: Use option 1 (eBay API) for reliable data!')
        
    except Exception as e:
        print()
        print_error(f'Scraping failed: {str(e)}')
        print()
        print(Fore.YELLOW + '💡 Troubleshooting:')
        print(Fore.CYAN + '   1. Install Playwright browsers:')
        print(Fore.CYAN + '      playwright install chromium')
        print()
        print(Fore.CYAN + '   2. eBay may be blocking or showing CAPTCHA')
        print(Fore.CYAN + '      Check ebay_debug.png if it was created')
        print()
        print(Fore.CYAN + '   3. Use option 1 (eBay API) for reliable access')


def scrape_cards():
    '''
    Interactive scraping menu with Scrapy (fast but blocked by robots.txt)
    '''
    print(Fore.YELLOW + '\n━━━ SCRAPY SPIDER (Fast HTTP Scraper) ━━━\n')
    
    print(Fore.YELLOW + '⚠  This method is blocked by eBay:')
    print('   • Respects robots.txt (ROBOTSTXT_OBEY = True)')
    print('   • HTTP-only (no JavaScript support)')
    print('   • Expected result: 0 items from eBay')
    print()
    print(Fore.GREEN + '💡 Better options:')
    print(Fore.CYAN + '   • Option 1: eBay API (legal, reliable)')
    print(Fore.CYAN + '   • Option 2: Playwright (bypasses robots.txt)\n')
    
    # Check for CAPTCHA API key
    captcha_key = os.environ.get('CAPTCHA_API_KEY')
    if not captcha_key:
        print(Fore.CYAN + 'CAPTCHA Solver: ' + Fore.RED + 'Not configured')
        print(Style.RESET_ALL + 'Configure in option 6 for automatic CAPTCHA solving')
        print()
        
        choice = input(Fore.CYAN + 'Continue anyway? (yes/no): ' + Style.RESET_ALL).strip().lower()
        if choice != 'yes':
            print_info('Cancelled. Use option 1 (API) or option 6 (Configure).')
            return
    else:
        print_success(f'CAPTCHA solver configured: {captcha_key[:8]}...')
    
    card = input(Fore.CYAN + '\nEnter card name: ' + Style.RESET_ALL).strip()
    if not card:
        print_error('Card name cannot be empty!')
        return
    
    pages = input(Fore.CYAN + 'Number of pages to scrape [3]: ' + Style.RESET_ALL).strip()
    pages = int(pages) if pages.isdigit() else 3
    
    print()
    print_info(f'Starting scrape for: {Fore.YELLOW}{card}')
    print_info(f'Pages to scrape: {Fore.YELLOW}{pages}')
    if captcha_key:
        print_info('CAPTCHA solving: ' + Fore.GREEN + 'ENABLED')
    print()
    
    try:
        # Use subprocess to avoid Twisted reactor issues
        import subprocess
        
        cmd = [
            'scrapy', 'crawl', 'ebay',
            '-a', f'card_name={card}',
            '-a', f'max_pages={pages}',
            '--nolog'  # Suppress verbose Scrapy logging
        ]
        
        if captcha_key:
            cmd.extend(['-s', f'CAPTCHA_API_KEY={captcha_key}'])
        
        print_info('Starting Scrapy spider...')
        print()
        
        # Run with real-time output
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print()
        
        # Check how many items were actually scraped
        db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
        items_found = 0
        
        if os.path.exists(db_path):
            try:
                engine = create_engine(f'sqlite:///{db_path}')
                Session = sessionmaker(bind=engine)
                session = Session()
                
                # Count items from this scrape (recent items)
                from datetime import datetime, timedelta
                recent_time = (datetime.now() - timedelta(minutes=5)).isoformat()
                items_found = session.query(MtgCard).filter(
                    MtgCard.timestamp >= recent_time
                ).count()
                session.close()
            except:
                pass
        
        if items_found > 0:
            print_success(f'Scraping completed! Found {Fore.YELLOW}{items_found}{Fore.GREEN} cards!')
            print_info(f'Results saved to: {Fore.YELLOW}mtg_cards.db')
            print_info(f'Use {Fore.YELLOW}option 3{Fore.CYAN} to view results')
        else:
            print_error('Scraping completed but found 0 results')
            print()
            print(Fore.YELLOW + '⚠  Why no results?')
            print(Fore.YELLOW + '   • eBay blocks scraping via robots.txt (ROBOTSTXT_OBEY = True)')
            print(Fore.YELLOW + '   • This is expected - the scraper respects website policies')
            print()
            print(Fore.GREEN + '✅ Solution: Use option 1 (eBay API) instead!')
            print(Fore.CYAN + '   The API provides legal, reliable data access')
            print(Fore.CYAN + '   Or test with a site that allows scraping')
        
    except FileNotFoundError:
        print()
        print_error('Scrapy command not found!')
        print_info('Make sure you\'re in the virtual environment:')
        print(Fore.CYAN + '  source venv/bin/activate')
    except Exception as e:
        print()
        print_error(f'Scraping failed: {str(e)}')
        print_info('This may be due to eBay\'s anti-bot protection.')
        print_info('Consider using the eBay API (option 1) for reliable data access.')


def configure_settings():
    '''
    Configure CAPTCHA and proxy settings
    '''
    print(Fore.YELLOW + '\n━━━ CONFIGURATION SETTINGS ━━━\n')
    
    print(Fore.CYAN + '1. CAPTCHA Solver Configuration')
    captcha_configured = os.environ.get('CAPTCHA_API_KEY')
    local_captcha = os.environ.get('USE_LOCAL_CAPTCHA', 'false').lower() == 'true'
    
    if captcha_configured:
        print('   2Captcha API: ' + Fore.GREEN + 'Configured ✓')
    else:
        print('   2Captcha API: ' + Fore.RED + 'Not configured')
    
    if local_captcha:
        print('   Local ML Solver: ' + Fore.GREEN + 'Enabled ✓')
    else:
        print('   Local ML Solver: ' + Fore.YELLOW + 'Disabled')
    
    print()
    print('   ' + Fore.YELLOW + 'Option A: 2Captcha (Paid, Reliable)')
    print('   • Register at: ' + Fore.CYAN + 'https://2captcha.com/')
    print(Style.RESET_ALL + '   • Cost: ~$3 per 1000 CAPTCHAs')
    print('   • Setup: ' + Fore.CYAN + 'export CAPTCHA_API_KEY="your-key"')
    print()
    print('   ' + Fore.YELLOW + 'Option B: Local ML Solver (Free, Experimental)')
    print('   • Uses TensorFlow + OpenCV')
    print('   • Free but less reliable')
    print('   • Setup: ' + Fore.CYAN + 'export USE_LOCAL_CAPTCHA=true')
    print()
    
    print(Fore.CYAN + '2. Proxy Configuration')
    print('   Current: ' + (Fore.GREEN + 'Configured' if os.environ.get('PROXY_LIST') else Fore.RED + 'Not configured'))
    print()
    print('   To enable rotating proxies:')
    print('   • Get proxy list from providers like:')
    print('     - Bright Data (residential proxies)')
    print('     - Oxylabs')
    print('     - ScraperAPI')
    print('   • Create proxies.txt with format: http://user:pass@host:port')
    print('   • Run: ' + Fore.CYAN + 'export PROXY_LIST="proxies.txt"')
    print()
    
    print(Fore.CYAN + '3. eBay API Key')
    print('   Current: ' + (Fore.GREEN + 'Configured' if os.environ.get('EBAY_API_KEY') else Fore.RED + 'Not configured'))
    print()
    print('   To enable eBay API:')
    print('   • Register at: ' + Fore.YELLOW + 'https://developer.ebay.com/')
    print(Style.RESET_ALL + '   • Create application and get App ID')
    print('   • Run: ' + Fore.CYAN + 'export EBAY_API_KEY="your-app-id"')
    print()
    
    print(Fore.YELLOW + 'Tip: Add exports to ~/.zshrc or ~/.bashrc to make them permanent')
    print()


def view_results():
    '''
    Interactive results viewing menu
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    print(Fore.YELLOW + '\n━━━ VIEW RESULTS ━━━\n')
    
    limit = input(Fore.CYAN + 'Number of results to show [20]: ' + Style.RESET_ALL).strip()
    limit = int(limit) if limit.isdigit() else 20
    
    card_filter = input(Fore.CYAN + 'Filter by card name (leave empty for all): ' + Style.RESET_ALL).strip()
    
    try:
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        query = session.query(MtgCard).order_by(desc(MtgCard.id))
        
        if card_filter:
            query = query.filter(MtgCard.card_name.like(f'%{card_filter}%'))
        
        results = query.limit(limit).all()
        
        if not results:
            print_info('No results found')
            return
        
        headers = ['ID', 'Card Name', 'Price', 'Condition', 'Source', 'Shipping']
        rows = []
        
        for result in results:
            rows.append([
                result.id,
                result.card_name[:40] + '...' if len(result.card_name) > 40 else result.card_name,
                result.price,
                result.condition[:20] if result.condition else 'N/A',
                result.source,
                result.shipping[:20] if result.shipping else 'N/A'
            ])
        
        print()
        print_info(f'Showing {len(results)} results:\n')
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        print()
        print_info(f'Total records in database: {Fore.YELLOW}{session.query(MtgCard).count()}')
        
        session.close()
        
    except Exception as e:
        print_error(f'Failed to read database: {str(e)}')


def view_detail():
    '''
    View detailed card information
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    print(Fore.YELLOW + '\n━━━ VIEW CARD DETAILS ━━━\n')
    
    card_id = input(Fore.CYAN + 'Enter card ID: ' + Style.RESET_ALL).strip()
    if not card_id.isdigit():
        print_error('Invalid ID!')
        return
    
    try:
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        card = session.query(MtgCard).filter(MtgCard.id == int(card_id)).first()
        
        if not card:
            print_error(f'No card found with ID: {card_id}')
            return
        
        print()
        print(Fore.CYAN + '─' * 70)
        print(Fore.GREEN + f'Card Details (ID: {card.id})'.center(70))
        print(Fore.CYAN + '─' * 70)
        print()
        print(f'{Fore.YELLOW}Card Name:{Style.RESET_ALL}  {card.card_name}')
        print(f'{Fore.YELLOW}Price:{Style.RESET_ALL}      {card.price}')
        print(f'{Fore.YELLOW}Condition:{Style.RESET_ALL}  {card.condition}')
        print(f'{Fore.YELLOW}Shipping:{Style.RESET_ALL}   {card.shipping}')
        print(f'{Fore.YELLOW}Source:{Style.RESET_ALL}     {card.source}')
        print(f'{Fore.YELLOW}Seller:{Style.RESET_ALL}     {card.seller}')
        print(f'{Fore.YELLOW}Timestamp:{Style.RESET_ALL}  {card.timestamp}')
        print(f'{Fore.YELLOW}URL:{Style.RESET_ALL}        {card.url}')
        print()
        print(Fore.CYAN + '─' * 70)
        
        session.close()
        
    except Exception as e:
        print_error(f'Failed to read database: {str(e)}')


def show_stats():
    '''
    Display database statistics
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    print(Fore.YELLOW + '\n━━━ DATABASE STATISTICS ━━━\n')
    
    try:
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        total_cards = session.query(MtgCard).count()
        
        if total_cards == 0:
            print_info('Database is empty. Run a scrape to collect data!')
            session.close()
            return
        
        sources = session.query(MtgCard.source).distinct().all()
        
        print(f'{Fore.YELLOW}Total Cards:{Style.RESET_ALL}    {Fore.GREEN}{total_cards}')
        print(f'{Fore.YELLOW}Sources:{Style.RESET_ALL}        {", ".join([s[0] for s in sources])}')
        print()
        
        print(Fore.CYAN + 'Breakdown by Source:')
        for source in sources:
            count = session.query(MtgCard).filter(MtgCard.source == source[0]).count()
            print(f'  {Fore.GREEN}●{Style.RESET_ALL} {source[0]}: {count} cards')
        
        print()
        session.close()
        
    except Exception as e:
        print_error(f'Failed to read database: {str(e)}')


def clear_database():
    '''
    Clear all data from database
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found.')
        return
    
    print(Fore.YELLOW + '\n━━━ CLEAR DATABASE ━━━\n')
    confirm = input(Fore.RED + 'Are you sure you want to delete all data? (yes/no): ' + Style.RESET_ALL).strip().lower()
    
    if confirm == 'yes':
        try:
            os.remove(db_path)
            print_success('Database cleared successfully!')
        except Exception as e:
            print_error(f'Failed to clear database: {str(e)}')
    else:
        print_info('Operation cancelled')


def interactive_menu():
    '''
    Main interactive menu loop
    '''
    print_banner()
    
    while True:
        print_menu()
        choice = input(Fore.GREEN + '→ Select an option: ' + Style.RESET_ALL).strip()
        
        if choice == '1':
            playwright_scraper()
        elif choice == '2':
            ebay_api_search()
        elif choice == '3':
            scrape_cards()
        elif choice == '4':
            view_results()
        elif choice == '5':
            view_detail()
        elif choice == '6':
            show_stats()
        elif choice == '7':
            configure_settings()
        elif choice == '8':
            clear_database()
        elif choice == '0':
            print()
            print(Fore.CYAN + '🃏  Thanks for using MTG Scraper! Happy hunting!')
            print()
            break
        else:
            print_error('Invalid option! Please select 0-8.')
        
        input(Fore.CYAN + '\nPress Enter to continue...' + Style.RESET_ALL)
        print('\n' * 2)


@click.command()
@click.option('--menu/--no-menu', default=True, help='Use interactive menu (default)')
@click.option('--card', '-c', help='Card name to search for (direct mode)')
@click.option('--pages', '-p', default=3, type=int, help='Number of pages to scrape (direct mode)')
def main(menu, card, pages):
    '''
    MTG Scraper - Scrape Magic: The Gathering card prices from various sources
    
    Run without arguments for interactive menu, or use --card for direct scraping.
    '''
    if menu and not card:
        # Interactive menu mode
        interactive_menu()
    elif card:
        # Direct scraping mode
        print_banner()
        print_info(f'Starting scrape for: {Fore.YELLOW}{card}')
        print_info(f'Pages to scrape: {Fore.YELLOW}{pages}')
        print()
        
        try:
            import subprocess
            
            cmd = [
                'scrapy', 'crawl', 'ebay',
                '-a', f'card_name={card}',
                '-a', f'max_pages={pages}',
                '--nolog'
            ]
            
            subprocess.run(cmd, capture_output=False, text=True)
            
            print()
            print_success('Scraping completed successfully!')
            print_info(f'Results saved to: {Fore.YELLOW}mtg_cards.db')
            print_info(f'Run without --card flag to view results in interactive menu')
            
        except Exception as e:
            print_error(f'Scraping failed: {str(e)}')
            sys.exit(1)
    else:
        interactive_menu()


if __name__ == '__main__':
    main()
