#!/usr/bin/env python3
"""
Gradient Showcase - Demonstrates all the beautiful gradients applied to MTG Scraper
Run this to see the gradient effects in action!
"""

from mtgscraper.colors import (
    Colors, gradient_text, cyber_gradient, purple_gradient,
    magic_gradient, fire_gradient, green_gradient, rainbow_gradient,
    sunset_gradient, ocean_gradient
)
import pyfiglet

def main():
    print("\n")
    
    # Banner
    banner = pyfiglet.figlet_format('MTG Scraper', font='slant')
    banner_lines = banner.split('\n')
    for line in banner_lines:
        if line.strip():
            print(cyber_gradient(line))
        else:
            print()
    
    # Separator
    separator = '═' * 80
    print(gradient_text(separator, (0, 255, 255), (200, 0, 255)))
    print()
    
    # Showcase different gradient styles
    print(gradient_text("🌟 GRADIENT SHOWCASE 🌟", (255, 215, 0), (255, 140, 0)).center(80))
    print()
    
    # Cyber gradient
    print(f"  {cyber_gradient('Cyber Gradient')} - Tech/Modern feel (Cyan → Blue)")
    print(f"  {purple_gradient('Purple Gradient')} - Premium feel (Blue → Purple)")
    print(f"  {magic_gradient('Magic Gradient')} - Magical feel (Purple → Pink)")
    print(f"  {fire_gradient('Fire Gradient')} - Alert/Warning (Yellow → Red)")
    print(f"  {green_gradient('Green Gradient')} - Success/Growth (Green → Cyan)")
    print(f"  {sunset_gradient('Sunset Gradient')} - Warm feel (Orange → Red)")
    print(f"  {ocean_gradient('Ocean Gradient')} - Cool feel (Blue → Cyan)")
    print(f"  {rainbow_gradient('Rainbow Gradient')} - Full spectrum!")
    print()
    
    # Status messages with gradients
    print(gradient_text("📊 STATUS MESSAGES:", (0, 255, 255), (100, 200, 255)))
    print()
    
    success_icon = gradient_text('✓', (0, 255, 0), (100, 255, 100))
    print(f"  {success_icon} {Colors.BRIGHT_GREEN}Success message - Operation completed!{Colors.RESET}")
    
    error_icon = gradient_text('✗', (255, 0, 0), (255, 100, 100))
    print(f"  {error_icon} {Colors.BRIGHT_RED}Error message - Something went wrong!{Colors.RESET}")
    
    info_icon = gradient_text('ℹ', (0, 255, 255), (100, 200, 255))
    print(f"  {info_icon} {Colors.BRIGHT_CYAN}Info message - Here's some information{Colors.RESET}")
    
    warning_icon = gradient_text('⚠', (255, 215, 0), (255, 165, 0))
    print(f"  {warning_icon} {Colors.BRIGHT_YELLOW}Warning message - Please be careful!{Colors.RESET}")
    print()
    
    # Section headers showcase
    print(gradient_text("📑 SECTION HEADERS:", (138, 43, 226), (255, 0, 255)))
    print()
    
    headers = [
        ("━━━ eBay BROWSE API (OAuth 2.0) ━━━", (0, 255, 255), (0, 150, 255)),
        ("━━━ PLAYWRIGHT BROWSER SCRAPER ━━━", (0, 255, 200), (150, 100, 255)),
        ("━━━ SCRAPY SPIDER (Fast HTTP Scraper) ━━━", (255, 100, 100), (255, 0, 0)),
        ("━━━ CONFIGURATION SETTINGS ━━━", (255, 215, 0), (255, 140, 0)),
        ("━━━ VIEW RESULTS ━━━", (0, 255, 255), (100, 200, 255)),
        ("━━━ DATABASE STATISTICS ━━━", (0, 255, 0), (100, 255, 100)),
        ("━━━ RUN DBT MODELS ━━━", (138, 43, 226), (255, 0, 255)),
        ("━━━ CLEAR DATABASE ━━━", (255, 0, 0), (255, 100, 100)),
    ]
    
    for text, start, end in headers:
        print(f"  {gradient_text(text, start, end)}")
    print()
    
    # Menu items showcase
    print(gradient_text("🎯 MENU ITEMS:", (0, 255, 0), (100, 255, 100)))
    print()
    
    opt1 = gradient_text('1.  ', (255, 215, 0), (255, 165, 0))
    rec = gradient_text('(Recommended)', (0, 255, 0), (100, 255, 100))
    print(f"  {opt1}{Colors.WHITE}Playwright Scraper {rec}{Colors.RESET}")
    
    opt2 = gradient_text('2.  ', (255, 215, 0), (255, 165, 0))
    api = gradient_text('(OAuth 2.0)', (0, 255, 255), (100, 200, 255))
    print(f"  {opt2}{Colors.WHITE}eBay Browse API {api}{Colors.RESET}")
    
    opt3 = gradient_text('3.  ', (255, 215, 0), (255, 165, 0))
    adv = gradient_text('(Advanced setup)', (255, 0, 0), (255, 100, 100))
    print(f"  {opt3}{Colors.WHITE}Scrapy Spider {adv}{Colors.RESET}")
    print()
    
    # Analyzer output showcase
    print(gradient_text("🔍 ANALYZER OUTPUT:", (0, 255, 255), (150, 100, 255)))
    print()
    
    container_text = gradient_text(f'   ✓ Containers:', (0, 255, 0), (100, 255, 100))
    print(f'{container_text} {Colors.BRIGHT_CYAN}s-item{Colors.RESET} ({Colors.BRIGHT_YELLOW}64 found{Colors.RESET})')
    
    price_text = gradient_text(f'   ✓ Prices:', (0, 255, 0), (100, 255, 100))
    print(f'{price_text} {Colors.BRIGHT_CYAN}.s-item__price{Colors.RESET} ({Colors.BRIGHT_YELLOW}64 found{Colors.RESET})')
    
    title_text = gradient_text(f'   ✓ Titles:', (0, 255, 0), (100, 255, 100))
    print(f'{title_text} {Colors.BRIGHT_CYAN}.s-item__title{Colors.RESET} ({Colors.BRIGHT_YELLOW}64 found{Colors.RESET})')
    
    sample_text = gradient_text(f'   ✓ Sample prices:', (0, 255, 0), (100, 255, 100))
    samples = ', '.join([gradient_text(s, (0, 255, 0), (100, 255, 200)) for s in ['$1,234.99', '$567.89', '$23.45']])
    print(f'{sample_text} {samples}')
    print()
    
    # Bottom separator
    print(gradient_text(separator, (200, 0, 255), (0, 255, 255)))
    
    # Farewell
    farewell = gradient_text('🃏  Thanks for viewing the gradient showcase! Enjoy your colorful scraping!', (0, 255, 255), (138, 43, 226))
    print(farewell)
    print()

if __name__ == '__main__':
    main()
