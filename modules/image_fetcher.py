import requests
import os
import json

# Carica impostazioni
with open(os.path.join('config', 'settings.json'), 'r', encoding='utf-8') as f:
    settings = json.load(f)

PIXABAY_API_KEY = settings.get('pixabay_api_key')

def fetch_image_url(keyword, lang='en', per_page=3):
    """
    Cerca un'immagine su Pixabay per la keyword e restituisce l’URL della prima trovata.
    """
    if not PIXABAY_API_KEY:
        raise ValueError("Pixabay API key non configurata in settings.json")
    url = "https://pixabay.com/api/"
    params = {
        'key': PIXABAY_API_KEY,
        'q': keyword,
        'lang': lang,
        'per_page': per_page,
        'image_type': 'photo',
        'safesearch': 'true'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    hits = data.get("hits", [])
    if hits:
        return hits[0]["largeImageURL"]
    return None

def download_image(image_url, dest_folder="output/images"):
    """
    Scarica l'immagine da image_url nella cartella dest_folder e restituisce il path locale.
    """
    if not image_url:
        return None
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(image_url.split("?")[0])
    path = os.path.join(dest_folder, filename)
    r = requests.get(image_url, stream=True)
    with open(path, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    return path

