import os
from dotenv import load_dotenv

# Carica automaticamente le variabili dal file .env
load_dotenv()

# Esempio di come leggere variabili ambiente:
wp_api_url = os.getenv('WP_API_URL')
wp_auth_token = os.getenv('WP_AUTH_TOKEN')
amazon_api_key = os.getenv('AMAZON_API_KEY')

import requests
import json
from .image_fetcher import fetch_image_url
from .video_fetcher import fetch_video_url
from .publish_manager import can_publish, mark_published  # <-- importiamo il manager

def publish_to_wp(title, content, slug, lang="it",
                  meta_title=None, meta_description=None,
                  category=None, add_media=True):
    # …


    from config.settings_loader import settings
    WP_SITE_URL   = settings.get('wp_site_url')
    WP_TOKEN      = settings.get('wp_token')

    # 1) Verifica se possiamo pubblicare questo articolo (draft vs publish e limiti)
    if not can_publish(lang, category):
        status = "draft"
    else:
        status = "publish"

    headers = {
        "Authorization": f"Bearer {WP_TOKEN}",
        "Content-Type":  "application/json"
    }

    # 2) Media (immagine e video)
    featured_media_url = video_url = None
    featured_media_id = None
    if add_media:
        try:
            featured_media_url = fetch_image_url(title, lang)
            video_url          = fetch_video_url(title, lang)
        except Exception as e:
            print(f"⚠️ Errore media: {e}")

    # video embed sotto titolo
    if video_url:
        video_embed = (
            f'<div style="text-align:center;">'
            f'<video controls width="100%">'
            f'<source src="{video_url}" type="video/mp4">'
            f'</video></div><br>'
        )
        content = f"{video_embed}\n{content}"

    # immagine in evidenza
    if featured_media_url:
        resp = requests.post(
            f"{WP_SITE_URL}/wp-json/wp/v2/media",
            headers={
                "Authorization":        f"Bearer {WP_TOKEN}",
                "Content-Disposition":  f"attachment; filename={slug}.jpg",
                "Content-Type":         "image/jpeg"
            },
            data=requests.get(featured_media_url).content
        )
        if resp.status_code in (200,201):
            featured_media_id = resp.json().get("id")

    # 3) Costruzione payload
    data = {
        "title":   title,
        "slug":    slug,
        "content": content,
        "status":  status,
        "categories": [],
        "lang":    lang,
    }
    if meta_title or meta_description:
        data["yoast_head_json"] = {}
        if meta_title:       data["yoast_head_json"]["title"]       = meta_title
        if meta_description: data["yoast_head_json"]["description"] = meta_description

    if featured_media_id:
        data["featured_media"] = featured_media_id

    # 4) Chiamata API
    res = requests.post(
        f"{WP_SITE_URL}/wp-json/wp/v2/posts",
        headers=headers,
        data=json.dumps(data)
    )
    if res.status_code not in (200,201):
        print(f"❌ Errore pubblicazione {title} ({lang}):", res.text)
        return

    print(f"✅ Pubblicato su WordPress: {title} ({lang}) – status: {status}")

    # 5) Se è stato veramente pubblicato, aggiorniamo i contatori
    if status == "publish":
        mark_published(lang, category)

