# modules/affiliate_api/amazon_affiliates.py

import os
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.partner_type import PartnerType
from paapi5_python_sdk.rest import ApiException

# Puoi parametrizzare questi valori in un .env o in settings.json
ACCESS_KEY   = os.getenv("PAAPI_ACCESS_KEY")
SECRET_KEY   = os.getenv("PAAPI_SECRET_KEY")
PARTNER_TAG  = os.getenv("PAAPI_PARTNER_TAG")
HOST         = "webservices.amazon.com"
REGION       = "us-east-1"

def fetch_amazon_products(keywords: str, item_count: int = 3):
    """
    Restituisce una lista di oggetti prodotto dal SearchItems della PAAPI 5.0.
    """
    api = DefaultApi(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        host=HOST,
        region=REGION
    )

    request = SearchItemsRequest(
        partner_tag=PARTNER_TAG,
        partner_type=PartnerType.ASSOCIATES,
        keywords=keywords,
        search_index="All",
        item_count=item_count,
        # resources=[...]  # aggiungi se ti servono immagini, prezzi, ecc.
    )

    try:
        response = api.search_items(request)
        # Se vuoi, trasformi response.search_result.items in un dict o modello tuo
        return response.search_result.items or []
    except ApiException as e:
        print(f"[Amazon PAAPI] Errore {e.status}: {e.body}")
        return []

