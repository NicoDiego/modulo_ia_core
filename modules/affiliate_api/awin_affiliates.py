import os
from dotenv import load_dotenv

# Carica automaticamente le variabili dal file .env
load_dotenv()

# Esempio di come leggere variabili ambiente:
wp_api_url = os.getenv('WP_API_URL')
wp_auth_token = os.getenv('WP_AUTH_TOKEN')
amazon_api_key = os.getenv('AMAZON_API_KEY')

# modules/affiliate_api/awin_affiliates.py

import os
import requests

AWIN_TOKEN     = os.getenv("AWIN_API_TOKEN")
AWIN_PUBLISHER = os.getenv("AWIN_PUBLISHER_ID")
BASE_URL       = f"https://api.awin.com/publishers/{AWIN_PUBLISHER}/search"

def fetch_awin_products(keyword: str, count: int = 3):
    """Restituisce fino a `count` prodotti Awin per `keyword`."""
    headers = {"Authorization": f"Bearer {AWIN_TOKEN}"}
    params  = {"q": keyword, "size": count}
    resp    = requests.get(BASE_URL, headers=headers, params=params)
    data    = resp.json().get("content", [])
    results = []
    for item in data[:count]:
        results.append({
            "nome":      item.get("title"),
            "url":       item.get("url"),
            "image_url": item.get("imageUrl"),
            "price":     item.get("price")
        })
    return results
