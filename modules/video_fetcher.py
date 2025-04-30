import requests
import os
import json

# Carica impostazioni (API keys)
with open(os.path.join('config', 'settings.json'), 'r', encoding='utf-8') as f:
    settings = json.load(f)

PIXABAY_API_KEY = settings.get('pixabay_api_key')

def fetch_video_url(keyword, lang='en', per_page=3):
    """
    Cerca un video su Pixabay per la keyword e restituisce l’URL del primo video trovato.
    """
    if not PIXABAY_API_KEY:
        raise ValueError("Pixabay API key non configurata in settings.json")
    url = "https://pixabay.com/api/videos/"
    params = {
        'key': PIXABAY_API_KEY,
        'q': keyword,
        'lang': lang,
        'per_page': per_page
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    hits = data.get("hits", [])
    if hits:
        # ritorna l’URL del video in formato “medium” (480p)
        return hits[0]["videos"]["medium"]["url"]
    return None

def download_video(video_url, dest_folder="output/videos"):
    """
    Scarica il video da video_url nella cartella dest_folder e restituisce il path locale.
    """
    if not video_url:
        return None
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(video_url.split("?")[0])
    path = os.path.join(dest_folder, filename)
    r = requests.get(video_url, stream=True)
    with open(path, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    return path


