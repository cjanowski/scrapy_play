'''
Intelligent page structure analyzer
Discovers selectors automatically by analyzing the page structure
'''

import re
from collections import Counter
from mtgscraper.colors import Colors, gradient_text


class PageStructureAnalyzer:
    '''
    Analyzes a page to automatically discover the best selectors
    '''
    
    def __init__(self, page):
        self.page = page
        self.discovered_selectors = {}
    
    def analyze(self):
        '''
        Analyze the page structure and discover selectors
        '''
        analyzing_text = gradient_text('   🔍 Analyzing page structure...', (0, 255, 255), (150, 100, 255))
        print(analyzing_text)
        
        # Use JavaScript to analyze the DOM
        analysis = self.page.evaluate(r'''
            () => {
                const analysis = {
                    prices: [],
                    titles: [],
                    links: [],
                    patterns: {}
                };
                
                // Find all elements with prices (contains $ and numbers)
                const allElements = document.querySelectorAll('*');
                const pricePattern = /\$[\d,]+\.?\d*/;
                const priceElements = [];
                
                allElements.forEach(el => {
                    const text = el.textContent.trim();
                    if (pricePattern.test(text) && text.length < 50) {
                        const classes = el.className;
                        const tag = el.tagName.toLowerCase();
                        priceElements.push({
                            selector: tag + (classes ? '.' + classes.split(' ').join('.') : ''),
                            text: text,
                            classes: classes
                        });
                    }
                });
                
                // Find common class patterns for prices
                const priceClasses = priceElements.map(p => p.classes).filter(c => c);
                const priceClassCounts = {};
                priceClasses.forEach(cls => {
                    cls.split(' ').forEach(c => {
                        if (c.includes('price')) {
                            priceClassCounts[c] = (priceClassCounts[c] || 0) + 1;
                        }
                    });
                });
                
                // Find most common price class
                let bestPriceClass = null;
                let maxCount = 0;
                for (const [cls, count] of Object.entries(priceClassCounts)) {
                    if (count > maxCount) {
                        maxCount = count;
                        bestPriceClass = cls;
                    }
                }
                
                analysis.prices = {
                    bestSelector: bestPriceClass ? '.' + bestPriceClass : '.s-item__price',
                    count: maxCount,
                    samples: priceElements.slice(0, 5).map(p => p.text)
                };
                
                // Find container elements that contain both prices and titles
                const priceSelector = bestPriceClass ? '.' + bestPriceClass : '.s-item__price';
                const priceElementsFound = document.querySelectorAll(priceSelector);
                const containerClasses = {};
                
                // Find parent containers that hold price elements
                priceElementsFound.forEach(priceEl => {
                    let parent = priceEl.parentElement;
                    // Walk up to find a container with "item" or "card" in class
                    for (let i = 0; i < 5 && parent; i++) {
                        const classes = parent.className;
                        if (classes && (classes.includes('item') || classes.includes('card'))) {
                            // Check if this parent also contains a title element
                            const hasTitle = parent.querySelector('[class*="title"], h2, h3');
                            if (hasTitle) {
                                classes.split(' ').forEach(cls => {
                                    if (cls && (cls.includes('item') || cls.includes('card')) && !cls.includes('__')) {
                                        containerClasses[cls] = (containerClasses[cls] || 0) + 1;
                                    }
                                });
                                break;
                            }
                        }
                        parent = parent.parentElement;
                    }
                });
                
                // Find best container class
                let bestContainerClass = null;
                maxCount = 0;
                for (const [cls, count] of Object.entries(containerClasses)) {
                    if (count > maxCount) {
                        maxCount = count;
                        bestContainerClass = cls;
                    }
                }
                
                // If no container found via price parents, try to infer from price/title classes
                if (!bestContainerClass || maxCount < 10) {
                    // Extract base class from price selector (e.g., s-card__price -> s-card)
                    if (bestPriceClass && bestPriceClass.includes('__')) {
                        const baseClass = bestPriceClass.split('__')[0];
                        const potentialContainers = document.querySelectorAll('.' + baseClass);
                        if (potentialContainers.length > 10) {
                            bestContainerClass = baseClass;
                            maxCount = potentialContainers.length;
                        }
                    }
                }
                
                analysis.patterns.containerClass = bestContainerClass || 's-item';
                analysis.patterns.containerCount = maxCount;
                
                // Analyze title patterns
                const headings = document.querySelectorAll('h1, h2, h3, h4, [role="heading"], [class*="title"]');
                const titleClasses = {};
                headings.forEach(h => {
                    h.className.split(' ').forEach(cls => {
                        if (cls && cls.includes('title')) {
                            titleClasses[cls] = (titleClasses[cls] || 0) + 1;
                        }
                    });
                });
                
                let bestTitleClass = null;
                maxCount = 0;
                for (const [cls, count] of Object.entries(titleClasses)) {
                    if (count > maxCount) {
                        maxCount = count;
                        bestTitleClass = cls;
                    }
                }
                
                analysis.titles = {
                    bestSelector: bestTitleClass ? '.' + bestTitleClass : '.s-item__title',
                    count: maxCount
                };
                
                return analysis;
            }
        ''')
        
        # Pretty output with gradients
        container_text = gradient_text(f'   ✓ Containers:', (0, 255, 0), (100, 255, 100))
        print(f'{container_text} {Colors.BRIGHT_CYAN}{analysis["patterns"]["containerClass"]}{Colors.RESET} ({Colors.BRIGHT_YELLOW}{analysis["patterns"]["containerCount"]} found{Colors.RESET})')
        
        price_text = gradient_text(f'   ✓ Prices:', (0, 255, 0), (100, 255, 100))
        print(f'{price_text} {Colors.BRIGHT_CYAN}{analysis["prices"]["bestSelector"]}{Colors.RESET} ({Colors.BRIGHT_YELLOW}{analysis["prices"]["count"]} found{Colors.RESET})')
        
        title_text = gradient_text(f'   ✓ Titles:', (0, 255, 0), (100, 255, 100))
        print(f'{title_text} {Colors.BRIGHT_CYAN}{analysis["titles"]["bestSelector"]}{Colors.RESET} ({Colors.BRIGHT_YELLOW}{analysis["titles"]["count"]} found{Colors.RESET})')
        
        if analysis['prices']['samples']:
            sample_text = gradient_text(f'   ✓ Sample prices:', (0, 255, 0), (100, 255, 100))
            samples = ', '.join([gradient_text(s, (0, 255, 0), (100, 255, 200)) for s in analysis["prices"]["samples"][:3]])
            print(f'{sample_text} {samples}')
        
        self.discovered_selectors = {
            'container': '.' + analysis['patterns']['containerClass'],
            'price': analysis['prices']['bestSelector'],
            'title': analysis['titles']['bestSelector']
        }
        
        return self.discovered_selectors
    
    def get_selectors(self):
        '''
        Get the discovered selectors
        '''
        return self.discovered_selectors
