'''
Scrapy middlewares for MTG Scraper
Includes CAPTCHA solving (2Captcha + local ML solver) and proxy rotation
'''

import logging
import os

# Optional imports - gracefully handle if not installed
try:
    from twocaptcha import TwoCaptcha
    TWOCAPTCHA_AVAILABLE = True
except ImportError:
    TWOCAPTCHA_AVAILABLE = False
    logging.warning('2captcha-python not installed. Run: pip install 2captcha-python')

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning('TensorFlow not installed. Run: pip install tensorflow')

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning('OpenCV not installed. Run: pip install opencv-python')


class CaptchaSolverMiddleware:
    '''
    Middleware to automatically solve CAPTCHAs
    Supports both 2Captcha API and local ML-based solver
    '''
    
    def __init__(self, api_key=None, use_local=False):
        self.api_key = api_key
        self.use_local = use_local
        self.solver = None
        self.local_solver = None
        self.logger = logging.getLogger(__name__)
        
        # Try 2Captcha first (paid service)
        if api_key and TWOCAPTCHA_AVAILABLE:
            try:
                self.solver = TwoCaptcha(api_key)
                self.logger.info('CAPTCHA solver initialized with 2Captcha API')
            except Exception as e:
                self.logger.warning(f'2Captcha initialization failed: {e}')
        elif api_key and not TWOCAPTCHA_AVAILABLE:
            self.logger.warning('2Captcha API key provided but package not installed')
            self.logger.info('Install with: pip install 2captcha-python')
        
        # Fall back to local ML solver
        if not self.solver or use_local:
            try:
                self.local_solver = LocalCaptchaSolver()
                self.logger.info('Local ML-based CAPTCHA solver initialized')
            except Exception as e:
                self.logger.warning(f'Local CAPTCHA solver unavailable: {e}')
    
    @classmethod
    def from_crawler(cls, crawler):
        '''
        Initialize middleware from crawler settings
        '''
        api_key = crawler.settings.get('CAPTCHA_API_KEY')
        use_local = crawler.settings.get('USE_LOCAL_CAPTCHA', False)
        return cls(api_key=api_key, use_local=use_local)
    
    def process_response(self, request, response, spider):
        '''
        Check if response contains CAPTCHA and solve it
        '''
        if not self.solver:
            return response
        
        # Check for common CAPTCHA indicators
        if self._has_captcha(response):
            spider.logger.info('CAPTCHA detected, attempting to solve...')
            try:
                # Solve CAPTCHA
                result = self._solve_captcha(response, request.url)
                if result:
                    spider.logger.info('CAPTCHA solved successfully!')
                    # Here you would typically resubmit the request with CAPTCHA solution
                    # Implementation depends on the specific CAPTCHA type
                else:
                    spider.logger.warning('CAPTCHA solving failed')
            except Exception as e:
                spider.logger.error(f'CAPTCHA solving error: {e}')
        
        return response
    
    def _has_captcha(self, response):
        '''
        Detect if response contains a CAPTCHA
        '''
        # Common CAPTCHA indicators
        captcha_keywords = [
            'recaptcha',
            'captcha',
            'g-recaptcha',
            'robot check',
            'verify you are human'
        ]
        
        body = response.text.lower()
        return any(keyword in body for keyword in captcha_keywords)
    
    def _solve_captcha(self, response, url):
        '''
        Solve CAPTCHA using available methods (2Captcha or local ML)
        '''
        # Extract sitekey if it's reCAPTCHA
        if 'recaptcha' in response.text.lower():
            # Try 2Captcha API first
            if self.solver:
                try:
                    # Extract sitekey from response HTML
                    import re
                    sitekey_match = re.search(r'data-sitekey="([^"]+)"', response.text)
                    if sitekey_match:
                        sitekey = sitekey_match.group(1)
                        result = self.solver.recaptcha(
                            sitekey=sitekey,
                            url=url
                        )
                        return result.get('code')
                except Exception as e:
                    self.logger.error(f'2Captcha solving failed: {e}')
            
            # Fall back to local solver
            if self.local_solver:
                try:
                    return self.local_solver.solve_recaptcha(response, url)
                except Exception as e:
                    self.logger.error(f'Local CAPTCHA solving failed: {e}')
        
        # Try image-based CAPTCHA with local solver
        elif self.local_solver:
            try:
                return self.local_solver.solve_image_captcha(response)
            except Exception as e:
                self.logger.error(f'Image CAPTCHA solving failed: {e}')
        
        return None


class LocalCaptchaSolver:
    '''
    Local ML-based CAPTCHA solver using TensorFlow/OpenCV
    Free alternative to paid services like 2Captcha
    '''
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        '''
        Load pre-trained CAPTCHA solving model
        In production, you'd train this on CAPTCHA datasets
        '''
        if not TENSORFLOW_AVAILABLE:
            self.logger.warning('TensorFlow not available - install with: pip install tensorflow')
            return
        
        try:
            # This is a placeholder - you would load a real trained model
            # self.model = tf.keras.models.load_model('captcha_model.h5')
            self.logger.info('CAPTCHA model loaded (placeholder)')
        except Exception as e:
            self.logger.warning(f'Could not load CAPTCHA model: {e}')
    
    def solve_image_captcha(self, response):
        '''
        Solve image-based CAPTCHAs using computer vision
        '''
        if not OPENCV_AVAILABLE or not TENSORFLOW_AVAILABLE:
            self.logger.warning('OpenCV or TensorFlow not available for image CAPTCHA solving')
            return None
        
        try:
            import numpy as np
            from PIL import Image
            import io
            
            # Extract CAPTCHA image from response
            # This is simplified - real implementation would extract the actual image
            self.logger.info('Attempting local image CAPTCHA solve...')
            
            # In production:
            # 1. Extract CAPTCHA image URL from HTML
            # 2. Download the image
            # 3. Preprocess with OpenCV
            # 4. Run through trained model
            # 5. Return predicted text
            
            return None  # Placeholder
        except Exception as e:
            self.logger.error(f'Image CAPTCHA processing error: {e}')
            return None
    
    def solve_recaptcha(self, response, url):
        '''
        Solve reCAPTCHA challenges
        Note: reCAPTCHA v3 is very difficult to solve locally
        This is mainly for demonstration
        '''
        self.logger.warning('reCAPTCHA solving requires 2Captcha API')
        self.logger.info('Local solving not effective for reCAPTCHA v2/v3')
        return None


class ProxyMiddleware:
    '''
    Middleware for rotating proxies
    '''
    
    def __init__(self, proxy_list_file=None):
        self.proxies = []
        self.current_proxy_index = 0
        
        if proxy_list_file:
            try:
                with open(proxy_list_file, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                logging.info(f'Loaded {len(self.proxies)} proxies from {proxy_list_file}')
            except Exception as e:
                logging.error(f'Failed to load proxy list: {e}')
    
    @classmethod
    def from_crawler(cls, crawler):
        '''
        Initialize middleware from crawler settings
        '''
        import os
        proxy_file = os.environ.get('PROXY_LIST')
        return cls(proxy_list_file=proxy_file)
    
    def process_request(self, request, spider):
        '''
        Attach a rotating proxy to each request
        '''
        if self.proxies:
            proxy = self.proxies[self.current_proxy_index]
            request.meta['proxy'] = proxy
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            spider.logger.debug(f'Using proxy: {proxy}')
