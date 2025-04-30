import requests
import random
from config.settings_loader import settings

WP_SITE_URL = settings.get('wp_site_url')
WP_TOKEN    = settings.get('wp_token')


def get_all_articles(lang="it"):
    """
    Recupera tutti gli articoli di una lingua specifica da WordPress.
    """
    headers = {
        "Authorization": f"Bearer {WP_TOKEN}",
        "Content-Type":  "application/json"
    }
    articles = []
    page = 1
    while True:
        url = f"{WP_SITE_URL}/wp-json/wp/v2/posts?lang={lang}&per_page=100&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        for post in data:
            articles.append({
                "id":    post.get("id"),
                "title": post.get("title", {}).get("rendered"),
                "slug":  post.get("slug"),
                "link":  post.get("link")
            })
        page += 1
    return articles


def pick_related_articles(all_articles, exclude_slug=None, num_related=3):
    """
    Sceglie in modo casuale un certo numero di articoli correlati,
    escludendo eventualmente un articolo specifico (quello corrente).
    """
    filtered = [a for a in all_articles if a.get("slug") != exclude_slug]
    if not filtered:
        return []
    return random.sample(filtered, min(len(filtered), num_related))
