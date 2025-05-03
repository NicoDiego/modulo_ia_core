import json
import logging
import os

import requests
from dotenv import load_dotenv

from config.settings_loader import settings
from .image_fetcher import fetch_image_url, ImageNotFoundError
from .video_fetcher import fetch_video_url, VideoNotFoundError
from .publish_manager import can_publish, mark_published


# Carico le variabili d’ambiente (meglio farlo qui, una sola volta)
load_dotenv()

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

# Costanti configurate a runtime
WP_SITE_URL = settings.get('wp_site_url')
WP_TOKEN    = settings.get('wp_token')


def publish_to_wp(
    title,
    content,
    slug,
    lang="it",
    meta_title=None,
    meta_description=None,
    category=None,
    add_media=True
):
    """
    Pubblica un articolo su WordPress (solo draft se superati i limiti)
    e gestisce featured image e video embed.
    """

    # 1) Decido lo status in base ai limiti
    status = "publish" if can_publish(lang, category) else "draft"

    headers = {
        "Authorization": f"Bearer {WP_TOKEN}",
        "Content-Type":  "application/json"
    }

    featured_media_id = None
    image_url = None
    video_url = None

    # 2) Provo a recuperare media (immagine + video)
    if add_media:
        try:
            image_url = fetch_image_url(title, lang)
        except ImageNotFoundError as e:
            logging.warning("Nessuna immagine trovata per '%s' (%s): %s", title, lang, e)

        try:
            video_url = fetch_video_url(title, lang)
        except VideoNotFoundError as e:
            logging.warning("Nessun video trovato per '%s' (%s): %s", title, lang, e)

    # 2a) Inserisco video embed all’inizio del contenuto
    if video_url:
        video_embed = (
            '<div style="text-align:center;">'
            '<video controls width="100%">'
            f'<source src="{video_url}" type="video/mp4">'
            '</video></div><br>\n'
        )
        content = video_embed + content

    # 2b) Carico featured image su WP
    if image_url:
        img_resp = requests.get(image_url)
        if img_resp.ok:
            resp = requests.post(
                f"{WP_SITE_URL}/wp-json/wp/v2/media",
                headers={
                    "Authorization":       f"Bearer {WP_TOKEN}",
                    "Content-Disposition": f"attachment; filename={slug}.jpg",
                    "Content-Type":        "image/jpeg"
                },
                data=img_resp.content
            )
            if resp.ok:
                featured_media_id = resp.json().get("id")
            else:
                logging.error(
                    "Upload immagine fallito per '%s' (%s): %s",
                    title, lang, resp.text
                )
        else:
            logging.error(
                "Download immagine fallito (%s): %s",
                image_url, img_resp.status_code
            )

    # 3) Costruisco il payload per il post
    payload = {
        "title":      title,
        "slug":       slug,
        "content":    content,
        "status":     status,
        "categories": [],
        "lang":       lang,
    }

    if meta_title or meta_description:
        payload["yoast_head_json"] = {}
        if meta_title:
            payload["yoast_head_json"]["title"] = meta_title
        if meta_description:
            payload["yoast_head_json"]["description"] = meta_description

    if featured_media_id:
        payload["featured_media"] = featured_media_id

    # 4) Invio la richiesta di pubblicazione
    post_resp = requests.post(
        f"{WP_SITE_URL}/wp-json/wp/v2/posts",
        headers=headers,
        json=payload
    )

    if not post_resp.ok:
        logging.error(
            "Pubblicazione fallita '%s' (%s): %s",
            title, lang, post_resp.text
        )
        return

    logging.info(
        "✅ Pubblicato su WP: '%s' (%s) — status: %s",
        title, lang, status
    )

    # 5) Aggiorno i contatori se ho effettivamente pubblicato
    if status == "publish":
        mark_published(lang, category)
