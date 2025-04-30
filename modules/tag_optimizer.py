import csv
import json
import requests

# Config settings
with open('config/settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)
SITE_URL = settings.get('wp_site_url')
TOKEN    = settings.get('wp_jwt_token')

def load_conversion_report(path='data/conversion_report.csv'):
    report = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            report.append(row)
    return report

def optimize_post_tags_and_categories(report, top_n=3):
    # pick top_n articles by revenue
    sorted_rep = sorted(report, key=lambda x: float(x['guadagno_totale']), reverse=True)
    top = sorted_rep[:top_n]
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    for item in top:
        title = item['titolo_articolo']
        # get post by slug (simple)
        slug = title.lower().replace(' ', '-')
        # fetch post ID
        resp = requests.get(f"{SITE_URL}/wp-json/wp/v2/posts?slug={slug}", headers=headers)
        posts = resp.json()
        if posts:
            post_id = posts[0]['id']
            # define tags and category based on title keywords
            tags = [word for word in title.split() if len(word) > 3][:5]
            cat = tags[0]
            data = {
                'tags': tags,
                'categories': [cat]
            }
            # update post
            requests.post(
                f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}",
                headers=headers,
                json=data
            )
            print(f"Optimized post {post_id}: tags={tags}, category={cat}")
