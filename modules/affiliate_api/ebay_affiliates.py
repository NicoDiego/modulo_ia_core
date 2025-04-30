import os
from dotenv import load_dotenv

# Carica automaticamente le variabili dal file .env
load_dotenv()

# Esempio di come leggere variabili ambiente:
wp_api_url = os.getenv('WP_API_URL')
wp_auth_token = os.getenv('WP_AUTH_TOKEN')
amazon_api_key = os.getenv('AMAZON_API_KEY')

# modules/affiliate_api/ebay_affiliates.py

import os
import requests

EBAY_TOKEN = os.getenv("EBAY_OAUTH_TOKEN")  # OAuth token per Browse API
SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

def fetch_ebay_products(keyword: str, count: int = 3):
    """Restituisce fino a `count` prodotti eBay per `keyword`."""
    headers = {
        "Authorization": f"Bearer {EBAY_TOKEN}",
        "Content-Type":  "application/json"
    }
    params = {"q": keyword, "limit": count}
    resp   = requests.get(SEARCH_URL, headers=headers, params=params).json()
    items  = resp.get("itemSummaries", [])[:count]
    results = []
    for it in items:
        price_data = it.get("price", {})
        price = f"{price_data.get('value', '')} {price_data.get('currency', '')}"
        results.append({
            "nome":      it.get("title"),
            "url":       it.get("itemWebUrl"),
            "image_url": it.get("image", {}).get("imageUrl"),
            "price":     price
        })
    return results
