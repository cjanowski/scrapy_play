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
from mtgscraper.colors import (
    Colors, gradient_text, cyber_gradient, purple_gradient, 
    magic_gradient, fire_gradient, green_gradient, rainbow_gradient,
    center_colored_text, visible_length, strip_ansi
)

# Initialize colorama
init(autoreset=True)


def print_banner():
    '''
    Display ASCII art banner with gradient effects
    '''
    banner = pyfiglet.figlet_format('MTG Scraper', font='slant')
    
    # Apply gradient to each line of the banner
    banner_lines = banner.split('\n')
    for line in banner_lines:
        if line.strip():
            # Cyber gradient for the ASCII art
            print(cyber_gradient(line))
        else:
            print()
    
    # Gradient separator
    separator = '═' * 70
    print(gradient_text(separator, (0, 255, 255), (200, 0, 255)))
    
    # Subtitle with magic gradient
    subtitle = ' Magic: The Gathering Card Price Scraper '
    gradient_subtitle = magic_gradient(subtitle)
    print(center_colored_text(gradient_subtitle, 70))
    
    # Bottom separator
    print(gradient_text(separator, (200, 0, 255), (0, 255, 255)))
    print()


def print_success(message):
    '''
    Print success message with gradient
    '''
    icon = gradient_text('✓', (0, 255, 0), (100, 255, 100))
    print(f'{icon} {Colors.BRIGHT_GREEN}{message}{Colors.RESET}')


def print_error(message):
    '''
    Print error message with gradient
    '''
    icon = gradient_text('✗', (255, 0, 0), (255, 100, 100))
    print(f'{icon} {Colors.BRIGHT_RED}{message}{Colors.RESET}')


def print_info(message):
    '''
    Print info message with gradient
    '''
    icon = gradient_text('ℹ', (0, 255, 255), (100, 200, 255))
    print(f'{icon} {Colors.BRIGHT_CYAN}{message}{Colors.RESET}')


# strip_ansi now imported from colors module


def format_menu_line(content, width=54):
    '''
    Format a menu line with proper padding
    content: the colored text content
    width: total width of the content area (default 54 for the box)
    '''
    # Calculate actual visible length without ANSI codes
    visible_length = len(strip_ansi(content))
    padding = ' ' * (width - visible_length)
    border_color = Colors.rgb(138, 43, 226)
    border = f'{border_color}║{Colors.RESET}'
    return border + content + padding + border


def print_menu():
    '''
    Display main menu with gradient effects
    '''
    # Border colors - solid purple for consistency
    border_color = Colors.rgb(138, 43, 226)
    
    # Create borders with solid corner characters and gradient middle
    top_corners = f'{border_color}╔'
    top_middle = gradient_text('══════════════════════════════════════════════════════', (138, 43, 226), (255, 0, 255))
    top_end = f'{border_color}╗{Colors.RESET}'
    border_top = top_corners + top_middle + top_end
    
    mid_corners = f'{border_color}╠'
    mid_middle = gradient_text('══════════════════════════════════════════════════════', (138, 43, 226), (255, 0, 255))
    mid_end = f'{border_color}╣{Colors.RESET}'
    border_mid = mid_corners + mid_middle + mid_end
    
    sep_corners = f'{border_color}╟'
    sep_middle = gradient_text('──────────────────────────────────────────────────────', (138, 43, 226), (200, 50, 255))
    sep_end = f'{border_color}╢{Colors.RESET}'
    border_sep = sep_corners + sep_middle + sep_end
    
    bot_corners = f'{border_color}╚'
    bot_middle = gradient_text('══════════════════════════════════════════════════════', (138, 43, 226), (255, 0, 255))
    bot_end = f'{border_color}╝{Colors.RESET}'
    border_bot = bot_corners + bot_middle + bot_end
    
    border_side = f'{border_color}║{Colors.RESET}'
    
    print(border_top)
    
    # Title with rainbow gradient
    title = rainbow_gradient('MAIN MENU')
    title_line = center_colored_text(title, 54)
    print(f'{border_side}{title_line}{border_side}')
    
    print(border_mid)
    
    # SCRAPING METHODS section
    section_title = gradient_text('SCRAPING METHODS', (0, 255, 0), (100, 255, 100))
    print(format_menu_line('  ' + section_title))
    print(border_sep)
    
    # Menu items with gradients
    opt1 = gradient_text('1.  ', (255, 215, 0), (255, 165, 0))
    text1 = gradient_text('Playwright Scraper', (100, 200, 255), (150, 150, 255))
    rec = gradient_text('(Recommended)', (0, 255, 0), (100, 255, 100))
    print(format_menu_line(f'  {opt1}{text1} {rec}{Colors.RESET}'))
    
    opt2 = gradient_text('2.  ', (255, 215, 0), (255, 165, 0))
    text2 = gradient_text('eBay Browse API', (100, 200, 255), (150, 150, 255))
    api = gradient_text('(OAuth 2.0)', (0, 255, 255), (100, 200, 255))
    print(format_menu_line(f'  {opt2}{text2} {api}{Colors.RESET}'))
    
    opt3 = gradient_text('3.  ', (255, 215, 0), (255, 165, 0))
    text3 = gradient_text('Scrapy Spider', (100, 200, 255), (150, 150, 255))
    adv = gradient_text('(Advanced setup)', (255, 0, 0), (255, 100, 100))
    print(format_menu_line(f'  {opt3}{text3} {adv}{Colors.RESET}'))
    
    print(border_sep)
    
    # VIEW & ANALYZE section
    section_title = gradient_text('VIEW & ANALYZE', (0, 150, 255), (100, 200, 255))
    print(format_menu_line('  ' + section_title))
    print(border_sep)
    
    for num, text in [('4.  ', 'View Results'), ('5.  ', 'View Card Details'), ('6.  ', 'Database Statistics')]:
        opt = gradient_text(num, (255, 215, 0), (255, 165, 0))
        text_gradient = gradient_text(text, (100, 200, 255), (150, 180, 255))
        print(format_menu_line(f'  {opt}{text_gradient}{Colors.RESET}'))
    
    print(border_sep)
    
    # DBT ANALYTICS section
    section_title = gradient_text('DBT ANALYTICS', (138, 43, 226), (255, 0, 255))
    print(format_menu_line('  ' + section_title))
    print(border_sep)
    
    opt7 = gradient_text('7.  ', (255, 215, 0), (255, 165, 0))
    text7 = gradient_text('Run dbt Models', (200, 150, 255), (255, 150, 255))
    transform = gradient_text('(Transform Data)', (0, 255, 0), (100, 255, 100))
    print(format_menu_line(f'  {opt7}{text7} {transform}{Colors.RESET}'))
    
    opt8 = gradient_text('8.  ', (255, 215, 0), (255, 165, 0))
    text8 = gradient_text('Run dbt Tests', (200, 150, 255), (255, 150, 255))
    quality = gradient_text('(Data Quality)', (0, 255, 255), (100, 200, 255))
    print(format_menu_line(f'  {opt8}{text8} {quality}{Colors.RESET}'))
    
    for num, text in [('9.  ', 'View Analytics Results'), ('10. ', 'Generate dbt Docs')]:
        opt = gradient_text(num, (255, 215, 0), (255, 165, 0))
        text_gradient = gradient_text(text, (200, 150, 255), (255, 150, 255))
        print(format_menu_line(f'  {opt}{text_gradient}{Colors.RESET}'))
    
    print(border_sep)
    
    # EXPORT & AUTOMATE section
    section_title = gradient_text('EXPORT & AUTOMATE', (0, 255, 255), (100, 255, 200))
    print(format_menu_line('  ' + section_title))
    print(border_sep)
    
    for num, text in [('11. ', 'Export to CSV'), ('12. ', 'Upload to S3'), 
                       ('13. ', 'Schedule Cron Job'), ('14. ', 'Remove Cron Jobs')]:
        opt = gradient_text(num, (255, 215, 0), (255, 165, 0))
        text_gradient = gradient_text(text, (100, 255, 200), (150, 255, 255))
        print(format_menu_line(f'  {opt}{text_gradient}{Colors.RESET}'))
    
    print(border_sep)
    
    # SETTINGS section
    section_title = gradient_text('SETTINGS', (255, 215, 0), (255, 140, 0))
    print(format_menu_line('  ' + section_title))
    print(border_sep)
    
    opt15 = gradient_text('15. ', (255, 215, 0), (255, 165, 0))
    text15 = gradient_text('Configure Settings', (255, 200, 100), (255, 180, 120))
    print(format_menu_line(f'  {opt15}{text15}{Colors.RESET}'))
    
    opt16 = gradient_text('16. ', (255, 215, 0), (255, 165, 0))
    text16 = gradient_text('Clear Database', (255, 200, 100), (255, 180, 120))
    warning = gradient_text('(Warning!)', (255, 0, 0), (255, 100, 100))
    print(format_menu_line(f'  {opt16}{text16} {warning}{Colors.RESET}'))
    
    print(border_sep)
    
    # EXIT
    opt0 = gradient_text('0.  ', (255, 0, 0), (255, 100, 100))
    text0 = gradient_text('Exit', (255, 100, 100), (255, 150, 150))
    print(format_menu_line(f'  {opt0}{text0}{Colors.RESET}'))
    
    print(border_bot)
    print()


def ebay_api_search():
    '''
    Search using eBay's official Browse API (RESTful, OAuth 2.0)
    '''
    import requests
    from datetime import datetime
    
    header = gradient_text('━━━ eBay BROWSE API (OAuth 2.0) ━━━', (0, 255, 255), (0, 150, 255))
    print(f'\n{header}\n')
    print_info('This uses eBay\'s modern RESTful API with OAuth')
    print()
    
    # Check for OAuth credentials
    client_id = os.environ.get('EBAY_CLIENT_ID')
    client_secret = os.environ.get('EBAY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print(Fore.YELLOW + '⚠  eBay OAuth Credentials Required\n')
        print('To use eBay\'s Browse API, you need to:')
        print('1. Register at: ' + Fore.CYAN + 'https://developer.ebay.com/')
        print(Style.RESET_ALL + '2. Create an application and get your credentials')
        print('3. Set environment variables:')
        print(Fore.CYAN + '   export EBAY_CLIENT_ID="your-app-id"')
        print(Fore.CYAN + '   export EBAY_CLIENT_SECRET="your-cert-id"')
        print()
        
        use_demo = input(Fore.CYAN + 'Use demo mode for testing? (yes/no): ' + Style.RESET_ALL).strip().lower()
        
        if use_demo == 'yes':
            client_id = 'DEMO_MODE'
            client_secret = 'DEMO_MODE'
            print_info('Using simulated API response for demonstration')
        else:
            print_info('Cancelled. Register at https://developer.ebay.com/ to get started!')
            return
    
    # Search options
    search_title = gradient_text('Search by:', (0, 255, 255), (100, 200, 255))
    print(search_title)
    print(gradient_text('  1. Card name', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  2. Set name', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  3. Card type', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  4. Custom MTG search', (100, 200, 255), (150, 150, 255)))
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
        if client_id == 'DEMO_MODE':
            # Simulated API response for demo purposes
            print_info('Simulating API call (demo mode)...')
            results = _simulate_ebay_api_response(card, limit)
        else:
            # Real API call with OAuth
            results = _call_ebay_browse_api(client_id, client_secret, card, limit)
        
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


def _get_ebay_oauth_token(client_id, client_secret):
    '''
    Get OAuth 2.0 access token for eBay Browse API
    '''
    import requests
    import base64
    
    # OAuth token endpoint
    token_url = 'https://api.ebay.com/identity/v1/oauth2/token'
    
    # Encode credentials
    credentials = f'{client_id}:{client_secret}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.ebay.com/oauth/api_scope'
    }
    
    response = requests.post(token_url, headers=headers, data=data, timeout=10)
    response.raise_for_status()
    
    token_data = response.json()
    return token_data['access_token']


def _call_ebay_browse_api(client_id, client_secret, keywords, limit):
    '''
    Call eBay's Browse API (RESTful with OAuth 2.0)
    '''
    import requests
    
    # Get OAuth token
    print_info('Getting OAuth access token...')
    access_token = _get_ebay_oauth_token(client_id, client_secret)
    print_success('OAuth token obtained!')
    print()
    
    # Browse API search endpoint
    search_url = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US',
        'Content-Type': 'application/json'
    }
    
    params = {
        'q': f'mtg {keywords}',
        'limit': str(min(limit, 200)),
        'sort': 'price'
    }
    
    response = requests.get(search_url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    
    results = []
    items = data.get('itemSummaries', [])
    
    for item in items:
        # Extract price
        price_info = item.get('price', {})
        price_value = price_info.get('value', '0')
        price_currency = price_info.get('currency', 'USD')
        
        # Extract shipping
        shipping_info = item.get('shippingOptions', [{}])[0] if item.get('shippingOptions') else {}
        shipping_cost = shipping_info.get('shippingCost', {})
        shipping_value = shipping_cost.get('value', '0')
        
        if shipping_value == '0' or shipping_value == '0.0':
            shipping_text = 'Free shipping'
        else:
            shipping_text = f'${shipping_value} shipping'
        
        results.append({
            'title': item.get('title', 'Unknown'),
            'price': f'${price_value}',
            'condition': item.get('condition', 'Not specified'),
            'url': item.get('itemWebUrl', ''),
            'shipping': shipping_text,
            'seller': item.get('seller', {}).get('username', 'Unknown')
        })
    
    return results


def playwright_scraper():
    '''
    Browser automation scraping with Playwright (bypasses many protections)
    '''
    header = gradient_text('━━━ PLAYWRIGHT BROWSER SCRAPER ━━━', (0, 255, 200), (150, 100, 255))
    print(f'\n{header}\n')
    
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
    search_title = gradient_text('Search by:', (0, 255, 255), (100, 200, 255))
    print(search_title)
    print(gradient_text('  1. Card name', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  2. Set name', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  3. Card type (creature, instant, etc.)', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  4. Custom search', (100, 200, 255), (150, 150, 255)))
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
    
    # Sorting options
    print()
    sort_title = gradient_text('Sort by:', (255, 215, 0), (255, 165, 0))
    print(sort_title)
    print(gradient_text('  1. Best Match (default)', (255, 200, 100), (255, 180, 100)))
    print(gradient_text('  2. Price: Highest First', (255, 200, 100), (255, 180, 100)))
    print(gradient_text('  3. Price: Lowest First', (255, 200, 100), (255, 180, 100)))
    print(gradient_text('  4. Newly Listed', (255, 200, 100), (255, 180, 100)))
    print(gradient_text('  5. Most Bids', (255, 200, 100), (255, 180, 100)))
    print()
    
    sort_choice = input(Fore.GREEN + 'Select sort option [1]: ' + Style.RESET_ALL).strip()
    sort_choice = sort_choice if sort_choice else '1'
    
    # eBay sort parameters
    sort_params = {
        '1': '',  # Best Match
        '2': '&_sop=16',  # Price + Shipping: highest first
        '3': '&_sop=15',  # Price + Shipping: lowest first
        '4': '&_sop=10',  # Time: newly listed
        '5': '&_sop=13',  # Number of bids: most first
    }
    sort_param = sort_params.get(sort_choice, '')
    
    limit = input(Fore.CYAN + '\nMax results [20]: ' + Style.RESET_ALL).strip()
    limit = int(limit) if limit.isdigit() else 20
    
    max_pages = input(Fore.CYAN + 'Max pages to scrape [5]: ' + Style.RESET_ALL).strip()
    max_pages = int(max_pages) if max_pages.isdigit() else 5
    
    headless_choice = input(Fore.CYAN + 'Run in background (headless)? [yes/no]: ' + Style.RESET_ALL).strip().lower()
    headless = headless_choice != 'no'
    
    print()
    print_info(f'Launching browser for: {Fore.YELLOW}{card}')
    
    # Show sort selection
    sort_names = {
        '1': 'Best Match',
        '2': 'Price: Highest First',
        '3': 'Price: Lowest First',
        '4': 'Newly Listed',
        '5': 'Most Bids'
    }
    print_info(f'Sort order: {Fore.YELLOW}{sort_names.get(sort_choice, "Best Match")}')
    print_info(f'Max pages: {Fore.YELLOW}{max_pages}')
    print_info(f'Max results per page: {Fore.YELLOW}{limit}')
    
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
            search_url = f'https://www.ebay.com/sch/i.html?_nkw=mtg+{card.replace(" ", "+")}&LH_BIN=1{sort_param}'
            print_info(f'Navigating to eBay...')
            
            # Pagination loop
            current_page = 1
            selectors = None
            
            while current_page <= max_pages and len(results) < limit * max_pages:
                try:
                    # Navigate to page
                    if current_page == 1:
                        page_url = search_url
                    else:
                        page_url = f'{search_url}&_pgn={current_page}'
                    
                    print_info(f'Scraping page {current_page}...')
                    page.goto(page_url, wait_until='domcontentloaded', timeout=30000)
                    
                    # Wait a bit for dynamic content
                    page.wait_for_timeout(3000)
                    
                    # Analyze page structure on first page
                    if current_page == 1:
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
                        break
                    
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
                                    
                                    // Get bid count
                                    const bidEl = listing.querySelector('.s-item__bids, .s-item__bidCount, [class*="bid"]');
                                    const bids = bidEl ? bidEl.textContent.trim() : '0 bids';
                                    
                                    // Get shipping info
                                    const shippingEl = listing.querySelector('.s-item__shipping, .s-item__freeXDays, [class*="shipping"]');
                                    const shipping = shippingEl ? shippingEl.textContent.trim() : 'See listing';
                                    
                                    // Get URL
                                    const linkEl = listing.querySelector('a.s-item__link, a[href*="/itm/"]');
                                    const url = linkEl ? linkEl.href : '';
                                    
                                    // Only include if we have title and price
                                    if (title && price && title.toLowerCase() !== 'shop on ebay' && price.includes('$')) {
                                        items.push({
                                            title: title,
                                            price: price,
                                            bids: bids,
                                            shipping: shipping,
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
                    print_info(f'JavaScript extracted {len(results_js)} items from page {current_page}')
                    
                    page_results = 0
                    for item in results_js:
                        if len(results) >= limit * max_pages:
                            break
                            
                        # Extract bid count for display
                        bid_info = item.get('bids', '0 bids')
                        has_bids = 'bid' in bid_info.lower() and bid_info.strip() != '0 bids'
                        
                        results.append({
                            'card_name': item['title'],
                            'price': item['price'],
                            'url': item['url'],
                            'source': 'eBay (Playwright)',
                            'timestamp': datetime.now().isoformat(),
                            'condition': bid_info if has_bids else 'Buy It Now',
                            'shipping': item.get('shipping', 'See listing'),
                            'buy_it_now': not has_bids,
                            'seller': 'eBay Seller',
                            'set_name': 'Unknown'
                        })
                        
                        # Display with bid info
                        bid_display = f' | {Fore.YELLOW}{bid_info}{Style.RESET_ALL}' if has_bids else ''
                        price_display = f' | {Fore.GREEN}{item["price"]}{Style.RESET_ALL}'
                        print(f'   {Fore.GREEN}✓{Style.RESET_ALL} {item["title"][:45]}{price_display}{bid_display}')
                        page_results += 1
                    
                    print_info(f'Collected {page_results} items from page {current_page}. Total so far: {len(results)}')
                    print()
                    
                    # Check if there's a next page
                    if current_page >= max_pages:
                        print_info(f'Reached max pages limit ({max_pages})')
                        break
                    
                    # Check for next page button
                    next_button = page.query_selector('a.pagination__next, nav.pagination a[aria-label="Next page"]')
                    if not next_button:
                        print_info('No more pages available')
                        break
                    
                    current_page += 1
                    
                except Exception as e:
                    print_error(f'Error on page {current_page}: {str(e)}')
                    # Save debug files if no results
                    if not results:
                        page.screenshot(path='ebay_debug.png')
                        with open('ebay_debug.html', 'w', encoding='utf-8') as f:
                            f.write(page.content())
                        print()
                        print_info('Debug files saved for inspection')
                    break
            
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
    header = gradient_text('━━━ SCRAPY SPIDER (Fast HTTP Scraper) ━━━', (255, 100, 100), (255, 0, 0))
    print(f'\n{header}\n')
    
    warning_title = gradient_text('⚠  This method is blocked by eBay:', (255, 215, 0), (255, 165, 0))
    print(warning_title)
    print(f'   {Colors.BRIGHT_YELLOW}• Respects robots.txt (ROBOTSTXT_OBEY = True){Colors.RESET}')
    print(f'   {Colors.BRIGHT_YELLOW}• HTTP-only (no JavaScript support){Colors.RESET}')
    print(f'   {Colors.BRIGHT_YELLOW}• Expected result: 0 items from eBay{Colors.RESET}')
    print()
    better_title = gradient_text('💡 Better options:', (0, 255, 0), (100, 255, 100))
    print(better_title)
    print(f'   {Colors.BRIGHT_CYAN}• Option 1: eBay API (legal, reliable){Colors.RESET}')
    print(f'   {Colors.BRIGHT_CYAN}• Option 2: Playwright (bypasses robots.txt){Colors.RESET}\n')
    
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
    header = gradient_text('━━━ CONFIGURATION SETTINGS ━━━', (255, 215, 0), (255, 140, 0))
    print(f'\n{header}\n')
    
    section1 = gradient_text('1. CAPTCHA Solver Configuration', (0, 255, 255), (100, 200, 255))
    print(section1)
    captcha_configured = os.environ.get('CAPTCHA_API_KEY')
    local_captcha = os.environ.get('USE_LOCAL_CAPTCHA', 'false').lower() == 'true'
    
    if captcha_configured:
        status = gradient_text('Configured ✓', (0, 255, 0), (100, 255, 100))
        print(f'   2Captcha API: {status}')
    else:
        status = gradient_text('Not configured', (255, 0, 0), (255, 100, 100))
        print(f'   2Captcha API: {status}')
    
    if local_captcha:
        status = gradient_text('Enabled ✓', (0, 255, 0), (100, 255, 100))
        print(f'   Local ML Solver: {status}')
    else:
        status = gradient_text('Disabled', (255, 215, 0), (255, 165, 0))
        print(f'   Local ML Solver: {status}')
    
    print()
    print(gradient_text('   Option A: 2Captcha (Paid, Reliable)', (255, 215, 0), (255, 165, 0)))
    print(gradient_text('   • Register at: https://2captcha.com/', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Cost: ~$3 per 1000 CAPTCHAs', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Setup: export CAPTCHA_API_KEY="your-key"', (200, 200, 200), (150, 150, 255)))
    print()
    print(gradient_text('   Option B: Local ML Solver (Free, Experimental)', (255, 215, 0), (255, 165, 0)))
    print(gradient_text('   • Uses TensorFlow + OpenCV', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Free but less reliable', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Setup: export USE_LOCAL_CAPTCHA=true', (200, 200, 200), (150, 150, 255)))
    print()
    
    section2 = gradient_text('2. Proxy Configuration', (0, 255, 255), (100, 200, 255))
    print(section2)
    if os.environ.get('PROXY_LIST'):
        status = gradient_text('Configured', (0, 255, 0), (100, 255, 100))
    else:
        status = gradient_text('Not configured', (255, 0, 0), (255, 100, 100))
    print(f'   Current: {status}')
    print()
    print(gradient_text('   To enable rotating proxies:', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Get proxy list from providers like:', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('     - Bright Data (residential proxies)', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('     - Oxylabs', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('     - ScraperAPI', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Create proxies.txt with format: http://user:pass@host:port', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Run: export PROXY_LIST="proxies.txt"', (200, 200, 200), (150, 150, 255)))
    print()
    
    section3 = gradient_text('3. eBay Browse API (OAuth 2.0)', (0, 255, 255), (100, 200, 255))
    print(section3)
    client_id = os.environ.get('EBAY_CLIENT_ID')
    client_secret = os.environ.get('EBAY_CLIENT_SECRET')
    
    if client_id and client_secret:
        status = gradient_text('Configured ✓', (0, 255, 0), (100, 255, 100))
    elif client_id or client_secret:
        status = gradient_text('Partially configured (missing one credential)', (255, 215, 0), (255, 165, 0))
    else:
        status = gradient_text('Not configured', (255, 0, 0), (255, 100, 100))
    print(f'   Current: {status}')
    
    print()
    print(gradient_text('   To enable eBay Browse API:', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Register at: https://developer.ebay.com/', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Create application and get OAuth credentials', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Run: export EBAY_CLIENT_ID="your-app-id"', (200, 200, 200), (150, 150, 255)))
    print(gradient_text('   • Run: export EBAY_CLIENT_SECRET="your-cert-id"', (200, 200, 200), (150, 150, 255)))
    print()
    
    tip = gradient_text('💡 Tip: Add exports to ~/.zshrc or ~/.bashrc to make them permanent', (255, 215, 0), (255, 140, 0))
    print(tip)
    print()


def view_results():
    '''
    Interactive results viewing menu
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    header = gradient_text('━━━ VIEW RESULTS ━━━', (0, 255, 255), (100, 200, 255))
    print(f'\n{header}\n')
    
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
    
    header = gradient_text('━━━ VIEW CARD DETAILS ━━━', (138, 43, 226), (255, 0, 255))
    print(f'\n{header}\n')
    
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
    
    header = gradient_text('━━━ DATABASE STATISTICS ━━━', (0, 255, 0), (100, 255, 100))
    print(f'\n{header}\n')
    
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


def export_to_csv():
    '''
    Export database results to CSV file on desktop
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    header = gradient_text('━━━ EXPORT TO CSV ━━━', (0, 255, 255), (100, 255, 200))
    print(f'\n{header}\n')
    
    try:
        import csv
        from datetime import datetime
        
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Get all results
        results = session.query(MtgCard).order_by(desc(MtgCard.id)).all()
        
        if not results:
            print_info('No results to export')
            session.close()
            return
        
        # Get desktop path
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'mtg_cards_{timestamp}.csv'
        csv_path = os.path.join(desktop_path, csv_filename)
        
        # Write CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'card_name', 'price', 'condition', 'seller', 'shipping', 'buy_it_now', 'url', 'source', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                writer.writerow({
                    'id': result.id,
                    'card_name': result.card_name,
                    'price': result.price,
                    'condition': result.condition,
                    'seller': result.seller,
                    'shipping': result.shipping,
                    'buy_it_now': result.buy_it_now,
                    'url': result.url,
                    'source': result.source,
                    'timestamp': result.timestamp
                })
        
        session.close()
        
        print_success(f'Exported {len(results)} records to CSV')
        print_info(f'File saved: {Fore.YELLOW}{csv_path}')
        print()
        
    except Exception as e:
        print_error(f'Export failed: {str(e)}')


def upload_to_s3():
    '''
    Upload CSV export to S3 bucket
    '''
    header = gradient_text('━━━ UPLOAD TO S3 ━━━', (255, 215, 0), (255, 140, 0))
    print(f'\n{header}\n')
    
    # Check for boto3
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
    except ImportError:
        print_error('boto3 not installed!')
        print()
        print('Install with:')
        print(Fore.CYAN + '  pip install boto3')
        print()
        return
    
    # Get S3 configuration
    s3_bucket = input(Fore.CYAN + 'S3 Bucket URL or name (e.g., s3://my-bucket or my-bucket): ' + Style.RESET_ALL).strip()
    
    if not s3_bucket:
        print_error('S3 bucket cannot be empty!')
        return
    
    # Parse bucket name
    if s3_bucket.startswith('s3://'):
        bucket_name = s3_bucket.replace('s3://', '').split('/')[0]
        prefix = '/'.join(s3_bucket.replace('s3://', '').split('/')[1:])
    else:
        bucket_name = s3_bucket.split('/')[0]
        prefix = '/'.join(s3_bucket.split('/')[1:])
    
    # Check for existing CSV or export new one
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    csv_files = [f for f in os.listdir(desktop_path) if f.startswith('mtg_cards_') and f.endswith('.csv')]
    
    if csv_files:
        csv_files.sort(reverse=True)
        use_existing = input(Fore.CYAN + f'Use existing CSV ({csv_files[0]})? [yes/no]: ' + Style.RESET_ALL).strip().lower()
        
        if use_existing == 'yes':
            csv_path = os.path.join(desktop_path, csv_files[0])
        else:
            print_info('Exporting new CSV...')
            export_to_csv()
            csv_files = [f for f in os.listdir(desktop_path) if f.startswith('mtg_cards_') and f.endswith('.csv')]
            csv_files.sort(reverse=True)
            csv_path = os.path.join(desktop_path, csv_files[0])
    else:
        print_info('No existing CSV found. Exporting...')
        export_to_csv()
        csv_files = [f for f in os.listdir(desktop_path) if f.startswith('mtg_cards_') and f.endswith('.csv')]
        if not csv_files:
            print_error('Failed to create CSV')
            return
        csv_files.sort(reverse=True)
        csv_path = os.path.join(desktop_path, csv_files[0])
    
    # Upload to S3
    try:
        s3_client = boto3.client('s3')
        
        # Construct S3 key
        filename = os.path.basename(csv_path)
        s3_key = f'{prefix}/{filename}' if prefix else filename
        
        print()
        print_info(f'Uploading to s3://{bucket_name}/{s3_key}...')
        
        s3_client.upload_file(csv_path, bucket_name, s3_key)
        
        print_success('Upload completed!')
        print_info(f'S3 URL: {Fore.YELLOW}s3://{bucket_name}/{s3_key}')
        print()
        
    except NoCredentialsError:
        print_error('AWS credentials not found!')
        print()
        print('Configure AWS credentials:')
        print(Fore.CYAN + '  aws configure')
        print(Style.RESET_ALL + 'Or set environment variables:')
        print(Fore.CYAN + '  export AWS_ACCESS_KEY_ID="your-key"')
        print(Fore.CYAN + '  export AWS_SECRET_ACCESS_KEY="your-secret"')
        print()
    except ClientError as e:
        print_error(f'S3 upload failed: {str(e)}')
        print()
    except Exception as e:
        print_error(f'Upload failed: {str(e)}')


def schedule_cron():
    '''
    Setup cron job for automated scraping
    '''
    header = gradient_text('━━━ SCHEDULE CRON JOB ━━━', (138, 43, 226), (255, 0, 255))
    print(f'\n{header}\n')
    
    print('This will create a cron job to run the scraper automatically.')
    print()
    
    # Get scraper settings
    method_title = gradient_text('Scraping method:', (0, 255, 255), (100, 200, 255))
    print(method_title)
    print(gradient_text('  1. Playwright (recommended)', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  2. eBay API', (100, 200, 255), (150, 150, 255)))
    print(gradient_text('  3. Scrapy', (100, 200, 255), (150, 150, 255)))
    print()
    
    method = input(Fore.GREEN + 'Select method [1]: ' + Style.RESET_ALL).strip()
    method = method if method else '1'
    
    card = input(Fore.CYAN + '\nCard name to search: ' + Style.RESET_ALL).strip()
    if not card:
        print_error('Card name cannot be empty!')
        return
    
    # Schedule frequency
    print()
    freq_title = gradient_text('Run frequency:', (138, 43, 226), (255, 0, 255))
    print(freq_title)
    print(gradient_text('  1. Every hour', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  2. Every 6 hours', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  3. Daily at specific time', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  4. Weekly on specific day', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  5. Custom cron expression', (200, 150, 255), (255, 150, 255)))
    print()
    
    freq = input(Fore.GREEN + 'Select frequency [1]: ' + Style.RESET_ALL).strip()
    freq = freq if freq else '1'
    
    # Build cron expression
    if freq == '1':
        cron_expr = '0 * * * *'  # Every hour
    elif freq == '2':
        cron_expr = '0 */6 * * *'  # Every 6 hours
    elif freq == '3':
        hour = input(Fore.CYAN + 'Hour (0-23): ' + Style.RESET_ALL).strip()
        cron_expr = f'0 {hour} * * *'  # Daily at specified hour
    elif freq == '4':
        day = input(Fore.CYAN + 'Day (0=Sun, 1=Mon, ..., 6=Sat): ' + Style.RESET_ALL).strip()
        hour = input(Fore.CYAN + 'Hour (0-23): ' + Style.RESET_ALL).strip()
        cron_expr = f'0 {hour} * * {day}'  # Weekly
    else:
        cron_expr = input(Fore.CYAN + 'Custom cron expression: ' + Style.RESET_ALL).strip()
    
    # Get script path
    script_path = os.path.abspath(__file__)
    python_path = sys.executable
    project_dir = os.getcwd()
    
    # Build command
    method_map = {
        '1': f'cd {project_dir} && {python_path} {script_path} --method playwright --card "{card}"',
        '2': f'cd {project_dir} && {python_path} {script_path} --method api --card "{card}"',
        '3': f'cd {project_dir} && {python_path} {script_path} --method scrapy --card "{card}"'
    }
    command = method_map.get(method, method_map['1'])
    
    # Optional: Export CSV after scraping
    export_csv = input(Fore.CYAN + '\nExport to CSV after each run? [yes/no]: ' + Style.RESET_ALL).strip().lower()
    if export_csv == 'yes':
        command += f' && {python_path} {script_path} --export-csv'
    
    # Optional: Upload to S3
    upload_s3 = input(Fore.CYAN + 'Upload to S3 after each run? [yes/no]: ' + Style.RESET_ALL).strip().lower()
    if upload_s3 == 'yes':
        s3_bucket = input(Fore.CYAN + 'S3 bucket URL: ' + Style.RESET_ALL).strip()
        os.environ['MTG_S3_BUCKET'] = s3_bucket
        command += f' && {python_path} {script_path} --upload-s3 {s3_bucket}'
    
    # Create cron entry
    cron_line = f'{cron_expr} {command} >> {project_dir}/cron.log 2>&1'
    
    print()
    print(Fore.CYAN + '─' * 70)
    print(Fore.YELLOW + 'Cron Job Configuration:')
    print(Fore.CYAN + '─' * 70)
    print()
    print(cron_line)
    print()
    print(Fore.CYAN + '─' * 70)
    print()
    
    confirm = input(Fore.GREEN + 'Add this cron job? [yes/no]: ' + Style.RESET_ALL).strip().lower()
    
    if confirm == 'yes':
        try:
            # Get current crontab
            import subprocess
            
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout if result.returncode == 0 else ''
            
            # Add new job
            new_cron = current_cron.rstrip() + '\n' + cron_line + '\n'
            
            # Write back
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=new_cron)
            
            print_success('Cron job added successfully!')
            print()
            print_info('View your cron jobs with: ' + Fore.YELLOW + 'crontab -l')
            print_info('Remove this job with: ' + Fore.YELLOW + 'crontab -e')
            print_info('Logs will be saved to: ' + Fore.YELLOW + f'{project_dir}/cron.log')
            print()
            
        except Exception as e:
            print_error(f'Failed to add cron job: {str(e)}')
            print()
            print('You can manually add this line to your crontab:')
            print(Fore.CYAN + f'  crontab -e')
            print(Style.RESET_ALL + 'Then add:')
            print(Fore.YELLOW + cron_line)
            print()
    else:
        print_info('Cron job not added')


def remove_cron():
    '''
    Remove scheduled cron jobs for MTG scraper
    '''
    import subprocess
    
    header = gradient_text('━━━ REMOVE CRON JOBS ━━━', (255, 0, 0), (255, 100, 100))
    print(f'\n{header}\n')
    
    script_path = os.path.abspath(__file__)
    
    try:
        # Get current crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print_info('No cron jobs found')
            return
        
        current_cron = result.stdout
        lines = current_cron.split('\n')
        
        # Find MTG scraper jobs
        mtg_jobs = []
        for i, line in enumerate(lines):
            if script_path in line and line.strip() and not line.strip().startswith('#'):
                mtg_jobs.append((i, line))
        
        if not mtg_jobs:
            print_info('No MTG scraper cron jobs found')
            return
        
        # Display jobs
        print(Fore.CYAN + 'Found the following MTG scraper cron jobs:\n')
        for idx, (_, job) in enumerate(mtg_jobs, 1):
            print(f'{Fore.YELLOW}{idx}. {Fore.WHITE}{job.strip()}')
        
        print()
        print(f'{Fore.YELLOW}0. {Fore.WHITE}Cancel')
        print()
        
        # Get user selection
        choice = input(Fore.GREEN + 'Select job to remove (or "all" to remove all): ' + Style.RESET_ALL).strip().lower()
        
        if choice == '0' or choice == 'cancel':
            print_info('Operation cancelled')
            return
        
        # Confirm removal
        if choice == 'all':
            confirm = input(Fore.RED + f'Remove ALL {len(mtg_jobs)} MTG scraper cron jobs? [yes/no]: ' + Style.RESET_ALL).strip().lower()
            if confirm != 'yes':
                print_info('Operation cancelled')
                return
            
            # Remove all MTG jobs
            indices_to_remove = [idx for idx, _ in mtg_jobs]
            new_lines = [line for i, line in enumerate(lines) if i not in indices_to_remove]
        else:
            try:
                job_num = int(choice)
                if job_num < 1 or job_num > len(mtg_jobs):
                    print_error('Invalid selection')
                    return
                
                idx_to_remove = mtg_jobs[job_num - 1][0]
                confirm = input(Fore.YELLOW + 'Remove this cron job? [yes/no]: ' + Style.RESET_ALL).strip().lower()
                
                if confirm != 'yes':
                    print_info('Operation cancelled')
                    return
                
                # Remove selected job
                new_lines = [line for i, line in enumerate(lines) if i != idx_to_remove]
            except ValueError:
                print_error('Invalid input')
                return
        
        # Write back updated crontab
        new_cron = '\n'.join(new_lines)
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        
        print_success('Cron job(s) removed successfully!')
        print()
        
    except Exception as e:
        print_error(f'Failed to remove cron job: {str(e)}')
        print()
        print('You can manually remove cron jobs with:')
        print(Fore.CYAN + '  crontab -e')
        print()


def run_dbt_models():
    '''
    Run dbt models to transform data
    '''
    header = gradient_text('━━━ RUN DBT MODELS ━━━', (138, 43, 226), (255, 0, 255))
    print(f'\n{header}\n')
    
    # Check if dbt is installed
    try:
        import subprocess
        result = subprocess.run(['dbt', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print_error('dbt is not installed!')
        print()
        print('Install dbt with:')
        print(Fore.CYAN + '  pip install dbt-core dbt-sqlite')
        print()
        return
    
    # Check if database exists
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    print_info('Running dbt models to transform your data...')
    print()
    
    try:
        import subprocess
        
        # Run dbt with profiles in current directory
        env = os.environ.copy()
        env['DBT_PROFILES_DIR'] = os.getcwd()
        
        result = subprocess.run(
            ['dbt', 'run', '--profiles-dir', '.'],
            capture_output=True,
            text=True,
            env=env
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print()
            print_success('dbt models completed successfully!')
            print_info('Analytics tables created:')
            print(Fore.CYAN + '  • card_price_stats - Price statistics by card')
            print(Fore.CYAN + '  • price_trends - Price changes over time')
            print(Fore.CYAN + '  • top_cards - Top cards by various metrics')
            print()
        else:
            print_error('dbt run failed!')
            print(result.stderr)
            
    except Exception as e:
        print_error(f'Failed to run dbt: {str(e)}')


def run_dbt_tests():
    '''
    Run dbt tests for data quality
    '''
    header = gradient_text('━━━ RUN DBT TESTS ━━━', (0, 255, 255), (100, 200, 255))
    print(f'\n{header}\n')
    
    print_info('Running data quality tests...')
    print()
    
    try:
        import subprocess
        
        env = os.environ.copy()
        env['DBT_PROFILES_DIR'] = os.getcwd()
        
        result = subprocess.run(
            ['dbt', 'test', '--profiles-dir', '.'],
            capture_output=True,
            text=True,
            env=env
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print()
            print_success('All tests passed! ✓')
        else:
            print()
            print_error('Some tests failed. Check output above.')
            
    except Exception as e:
        print_error(f'Failed to run tests: {str(e)}')


def view_dbt_analytics():
    '''
    View dbt analytics results
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found. Run a scrape first!')
        return
    
    header = gradient_text('━━━ DBT ANALYTICS RESULTS ━━━', (138, 43, 226), (255, 0, 255))
    print(f'\n{header}\n')
    
    select_title = gradient_text('Select analytics to view:', (138, 43, 226), (255, 0, 255))
    print(select_title)
    print(gradient_text('  1. Card Price Statistics', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  2. Price Trends Over Time', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  3. Top Cards (Hottest Cards)', (200, 150, 255), (255, 150, 255)))
    print(gradient_text('  4. Custom SQL Query', (200, 150, 255), (255, 150, 255)))
    print()
    
    choice = input(Fore.GREEN + 'Select option [1]: ' + Style.RESET_ALL).strip()
    choice = choice if choice else '1'
    
    try:
        from sqlalchemy import text
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if choice == '1':
            # Card price statistics
            result = session.execute(text('SELECT * FROM card_price_stats ORDER BY avg_price DESC LIMIT 20'))
            rows = result.fetchall()
            
            if rows:
                print()
                print_info('Top 20 Cards by Average Price:\n')
                headers = ['Card Name', 'Set', 'Listings', 'Min $', 'Avg $', 'Max $', 'Spread']
                table_rows = []
                for row in rows:
                    table_rows.append([
                        row[0][:30],  # card_name
                        row[1][:15],  # set_name
                        row[2],       # listing_count
                        f'${row[3]:.2f}',   # min_price
                        f'${row[5]:.2f}',   # avg_price
                        f'${row[4]:.2f}',   # max_price
                        f'${row[12]:.2f}'   # price_spread
                    ])
                print(tabulate(table_rows, headers=headers, tablefmt='grid'))
            else:
                print_info('No analytics data. Run dbt models first (option 7)!')
                
        elif choice == '2':
            # Price trends
            card_filter = input(Fore.CYAN + '\nEnter card name (leave empty for all): ' + Style.RESET_ALL).strip()
            
            if card_filter:
                result = session.execute(
                    text(f"SELECT * FROM price_trends WHERE card_name LIKE '%{card_filter}%' ORDER BY scraped_date DESC LIMIT 30")
                )
            else:
                result = session.execute(text('SELECT * FROM price_trends ORDER BY scraped_date DESC LIMIT 30'))
            
            rows = result.fetchall()
            
            if rows:
                print()
                print_info('Price Trends (Last 30 Days):\n')
                headers = ['Date', 'Card', 'Avg $', 'Change $', 'Change %']
                table_rows = []
                for row in rows:
                    change_pct = f"{row[6]:.1f}%" if row[6] else 'N/A'
                    table_rows.append([
                        row[2],       # date
                        row[0][:30],  # card_name
                        f'${row[4]:.2f}',   # avg_price
                        f'${row[5]:.2f}' if row[5] else 'N/A',   # change
                        change_pct
                    ])
                print(tabulate(table_rows, headers=headers, tablefmt='grid'))
            else:
                print_info('No trend data. Run dbt models first (option 7)!')
                
        elif choice == '3':
            # Top cards
            result = session.execute(text('SELECT * FROM top_cards ORDER BY hotness_score DESC LIMIT 20'))
            rows = result.fetchall()
            
            if rows:
                print()
                print_info('Top 20 Hottest Cards (by price × volume):\n')
                headers = ['Rank', 'Card Name', 'Avg $', 'Listings', 'Hotness']
                table_rows = []
                for idx, row in enumerate(rows, 1):
                    table_rows.append([
                        idx,
                        row[0][:35],  # card_name
                        f'${row[2]:.2f}',   # avg_price
                        row[3],       # listing_count
                        f'{row[11]:.0f}'    # hotness_score
                    ])
                print(tabulate(table_rows, headers=headers, tablefmt='grid'))
            else:
                print_info('No analytics data. Run dbt models first (option 7)!')
                
        elif choice == '4':
            # Custom query
            print()
            print(Fore.CYAN + 'Available tables:')
            print('  • stg_mtg_cards - Staging data')
            print('  • dim_cards - Card dimension')
            print('  • fct_card_prices - Price facts')
            print('  • card_price_stats - Price statistics')
            print('  • price_trends - Trends over time')
            print('  • top_cards - Top cards')
            print()
            
            query = input(Fore.GREEN + 'Enter SQL query: ' + Style.RESET_ALL).strip()
            
            if query:
                result = session.execute(text(query))
                rows = result.fetchall()
                
                if rows:
                    print()
                    print(tabulate(rows, tablefmt='grid'))
                else:
                    print_info('No results')
        
        session.close()
        
    except Exception as e:
        print_error(f'Failed to query analytics: {str(e)}')
        print()
        print_info('Make sure you\'ve run dbt models first (option 7)')


def generate_dbt_docs():
    '''
    Generate dbt documentation
    '''
    header = gradient_text('━━━ GENERATE DBT DOCUMENTATION ━━━', (0, 255, 200), (150, 100, 255))
    print(f'\n{header}\n')
    
    print_info('Generating dbt documentation...')
    print()
    
    try:
        import subprocess
        
        env = os.environ.copy()
        env['DBT_PROFILES_DIR'] = os.getcwd()
        
        # Generate docs
        result = subprocess.run(
            ['dbt', 'docs', 'generate', '--profiles-dir', '.'],
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print_success('Documentation generated!')
            print()
            
            serve = input(Fore.CYAN + 'Start documentation server? [yes/no]: ' + Style.RESET_ALL).strip().lower()
            
            if serve == 'yes':
                print()
                print_info('Starting documentation server...')
                print_info('Opening browser at http://localhost:8080')
                print_info('Press Ctrl+C to stop the server')
                print()
                
                subprocess.run(
                    ['dbt', 'docs', 'serve', '--profiles-dir', '.', '--port', '8080'],
                    env=env
                )
        else:
            print_error('Failed to generate docs')
            print(result.stderr)
            
    except KeyboardInterrupt:
        print()
        print_info('Documentation server stopped')
    except Exception as e:
        print_error(f'Failed to generate docs: {str(e)}')


def clear_database():
    '''
    Clear all data from database
    '''
    db_path = os.path.join(os.getcwd(), 'mtg_cards.db')
    
    if not os.path.exists(db_path):
        print_error('No database found.')
        return
    
    header = gradient_text('━━━ CLEAR DATABASE ━━━', (255, 0, 0), (255, 100, 100))
    print(f'\n{header}\n')
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
            run_dbt_models()
        elif choice == '8':
            run_dbt_tests()
        elif choice == '9':
            view_dbt_analytics()
        elif choice == '10':
            generate_dbt_docs()
        elif choice == '11':
            export_to_csv()
        elif choice == '12':
            upload_to_s3()
        elif choice == '13':
            schedule_cron()
        elif choice == '14':
            remove_cron()
        elif choice == '15':
            configure_settings()
        elif choice == '16':
            clear_database()
        elif choice == '0':
            print()
            farewell = gradient_text('🃏  Thanks for using MTG Scraper! Happy hunting!', (0, 255, 255), (138, 43, 226))
            print(farewell)
            print()
            break
        else:
            print_error('Invalid option! Please select 0-16.')
        
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
