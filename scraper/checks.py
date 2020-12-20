from bs4 import BeautifulSoup
from enum import Enum
import logging
import re
import requests
from urllib.parse import urlsplit

logger = logging.getLogger('yasps')

# SCRAPER CLASSES

class ItemAvailability(Enum):
    Unknown = 0
    OutOfStock = 1
    InStock = 2
    Reseller = 3

class MonitorItemAvailability:
    def __init__(self, item, targetPrice, checks, differentItems = False): 
        self.item = item 
        self.targetPrice = targetPrice
        self.checks = checks
        self.differentItems = differentItems
    def get_count(self):
        return len(self.checks)
		
class ShopItemStatus: 
    def __init__(self, availability, shop, price): 
        self.availability = availability 
        self.shop = shop
        self.price = price

# Parent class for web scraping

class Check: 
    def __init__(self, item, shop, url): 
        self.item = item
        self.shop = shop
        self.url = url
    def run(self):
        return ShopItemStatus(ItemAvailability.Unknown, self.shop, None)

# Advanced checkers that use BeautifulSoup

class CheckSoup(Check):
    def __init__(self, item, shop, url): 
        super().__init__(item, shop, url)
    def run(self):
        try:
            req = request_item(self.url, self.shop)
        except:
            return ShopItemStatus(ItemAvailability.Unknown, self.shop, None)
        soup = BeautifulSoup(req.text, "html.parser")
        availability = self.get_availability(soup)
        price = self.get_price(soup)
        return ShopItemStatus(availability, self.shop, price)
		
class Check_PCComponentes(CheckSoup):
    def __init__(self, item, url):
        super().__init__(item, 'PCComponentes', url)
    def get_availability(self, soup):
	    button_comprar = soup.find("button", {'data-loading-text':'Añadiendo...'})
	    if button_comprar:
	        availability = ItemAvailability.InStock if 'Comprar' in button_comprar.get_text(strip=True) else ItemAvailability.OutOfStock
	    else:
	        availability = ItemAvailability.Unknown
	    return availability
    def get_price(self, soup):
        button_comprar = soup.find("button", {'data-loading-text':'Añadiendo...'})
        if button_comprar:
            price = get_price(button_comprar['data-price'])
        else:
            price = None
        return price
    
class Check_Wipoid(CheckSoup):
    def __init__(self, item, url):
        super().__init__(item, 'Wipoid', url)
    def get_availability(self, soup):
	    button_comprar = soup.find("p", id = "add_to_cart")
	    if button_comprar:
	        availability = ItemAvailability.InStock if 'unvisible' not in button_comprar['class'] else ItemAvailability.OutOfStock
	    else:
	        availability = ItemAvailability.Unknown
	    return availability
    def get_price(self, soup):
        price_soup = soup.find("span", {'itemprop':'price'})
        if price_soup:
            price = get_price(price_soup['content'])
        else:
            price = None
        return price
    
class Check_Coolmod(CheckSoup):
    def __init__(self, item, url):
        super().__init__(item, 'Coolmod', url)
    def get_availability(self, soup):
        availability_soup = soup.find("span", class_ = "product-availability")
        if availability_soup:
            availability = ItemAvailability.InStock if 'Inmediato' in availability_soup.get_text(strip=True) else ItemAvailability.OutOfStock
        else:
            availability = ItemAvailability.Unknown
        return availability
    def get_price(self, soup):
        price_soup = soup.find("span", id = "hidden_price")
        if price_soup:
            price = get_price(price_soup.get_text(strip=True))
        else:
            price = None
        return price

# Basic checkers based on Regular expressions

class CheckRE(Check):
    def __init__(self, item, shop, url): 
        super().__init__(item, shop, url)
    def run(self):
        try:
            req = request_item(self.url, self.shop)
        except:
            return ShopItemStatus(ItemAvailability.Unknown, self.shop, None)
        inStock = not (self.sinStock in req.text)
        availability = ItemAvailability.InStock if inStock else ItemAvailability.OutOfStock
        price = get_price(req.text, self.priceRE)
        if (price is None) and (self.priceResellerRE is not None):
            price = get_price(req.text, self.priceResellerRE)
            if availability == ItemAvailability.InStock and price is not None:
                availability = ItemAvailability.Reseller
            else:
                availability = ItemAvailability.OutOfStock
        return ShopItemStatus(availability, self.shop, price)

class Check_VSGamers(CheckRE):
    def __init__(self, item, url):
        super().__init__(item, 'VSGamers', url)
        self.sinStock = '<meta itemprop="availability" content="outOfStock" />'
        self.priceRE = '<meta itemprop="price" content="(\d+\.?\d*)" />'

class Check_Alternate(CheckRE):
    def __init__(self, item, url):
        super().__init__(item, 'Alternate', url)
        self.sinStock = '<meta itemprop="availability" content="OutOfStock" />'
        self.priceRE = '<span itemprop="price" content="(\d+\.?\d*)"'

class Check_Amazon(CheckRE):
    def __init__(self, item, url):
        super().__init__(item, 'Amazon', url)
        self.sinStock = '<span class="a-size-medium a-color-price">No disponible.</span>'
        self.priceRE = '<span itemprop="price" content="(\d+\.?\d*)"'
        self.priceResellerRE = '<span class="a-size-base a-color-price">(\d+[\.,]?\d?\d?)'

class Check_Neobyte(CheckRE):
    def __init__(self, item, url):
        super().__init__(item, 'Neobyte', url)
        self.sinStock = '<span id="availability_value" class="label label-danger">No disponible</span>'
        self.priceRE = '<span id="our_price_display" class="price" itemprop="price" content="(\d+\.?\d?\d?)\d*"'

# Wrapper to assign object from URL

def getCheck(item, url):
    if url.startswith('https://www.pccomponentes.com/'):
        return Check_PCComponentes(item, url)
    elif url.startswith('https://www.neobyte.es/'):
        return Check_Neobyte(item, url)
    elif url.startswith('https://www.vsgamers.es/'):
        return Check_VSGamers(item, url)
    elif url.startswith('https://www.wipoid.com/'):
        return Check_Wipoid(item, url)
    elif url.startswith('https://www.amazon.es/'):
        return Check_Amazon(item, url)
    elif url.startswith('https://www.coolmod.com/'):
        return Check_Coolmod(item, url)
    elif url.startswith('https://www.alternate.es/'):
        return Check_Alternate(item, url)
    else:
        return Check(item, '', url)

# Auxiliar functions

def get_price(text, expr = '(\d+\.?\d?\d?)'):
    m = re.search(expr, text.replace(",", "."))
    if m:
        return float(m.group(1))
    else:
        return None


# REQUEST

def request_item(url, shop):
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': base_url,
        'accept-language': 'es-ES, es;q=0.9, en;q=0.8',
    }
    try:
        req = requests.get(url, timeout=10, headers=headers)
        req.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.info(f"{shop} returned {str(req.status_code)}")
        raise
    except requests.exceptions.ConnectionError as errc:
        logger.info(f"{shop} Connection Error")
        raise
    except requests.exceptions.Timeout as errt:
        logger.info(f"{shop} Connection Timeout")
        raise
    except:
        logger.info(f"{shop} Request Error")
        raise
    return req
