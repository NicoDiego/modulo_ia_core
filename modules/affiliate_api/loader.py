# modules/affiliate_api/loader.py

from .amazon_affiliates import fetch_amazon_products
from .awin_affiliates   import fetch_awin_products
from .ebay_affiliates   import fetch_ebay_products

def load_affiliate_links(keywords, per_source=2):
    """
    Per ogni keyword, interroga Amazon, Awin e eBay e
    restituisce una lista unificata di prodotti:
    [{ 'nome':…, 'url':…, 'image_url':…, 'price':… }, …]
    """
    links = []
    for kw in keywords:
        links += fetch_amazon_products(kw, per_source)
        links += fetch_awin_products(kw, per_source)
        links += fetch_ebay_products(kw, per_source)
    return links
