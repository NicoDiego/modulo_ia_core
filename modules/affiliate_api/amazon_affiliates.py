import os
from dotenv import load_dotenv

# Carica automaticamente le variabili dal file .env
load_dotenv()

# Esempio di come leggere variabili ambiente:
wp_api_url = os.getenv('WP_API_URL')
wp_auth_token = os.getenv('WP_AUTH_TOKEN')
amazon_api_key = os.getenv('AMAZON_API_KEY')


# modules/affiliate_api/amazon_affiliates.py

import os
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.configuration import Configuration
from paapi5_python_sdk.models import SearchItemsRequest, PartnerType

# Carica credenziali da env o da config/settings_loader
ACCESS_KEY    = os.getenv("AMAZON_PAAPI_ACCESS_KEY")
SECRET_KEY    = os.getenv("AMAZON_PAAPI_SECRET_KEY")
PARTNER_TAG   = os.getenv("AMAZON_PAAPI_PARTNER_TAG")
HOST          = "webservices.amazon.it"
REGION        = "eu-west-1"

def fetch_amazon_products(keyword: str, count: int = 3):
    """Restituisce fino a `count` prodotti Amazon per `keyword`."""
    conf = Configuration(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        host=HOST,
        region=REGION
    )
    api = DefaultApi(api_client=conf.get_api_client())
    request = SearchItemsRequest(
        Keywords=keyword,
        SearchIndex="All",
        ItemCount=count,
        PartnerTag=PARTNER_TAG,
        PartnerType=PartnerType.ASSOCIATES
    )
    response = api.search_items(request)
    results = []
    for item in response.search_result.items[:count]:
        title      = item.item_info.title.display_value
        url        = item.detail_page_url
        image_url  = item.images.primary.large.url
        price      = item.offers.listings[0].price.display_amount
        results.append({
            "nome": title,
            "url":   url,
            "image_url": image_url,
            "price": price
        })
    return results

