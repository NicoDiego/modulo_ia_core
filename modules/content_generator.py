import openai
import json

# Carica chiave API da settings.json
with open("config/settings.json", "r") as f:
    settings = json.load(f)
openai.api_key = settings["openai_api_key"]

def generate_article(topic, language="it"):
    prompt = (
        f"Scrivi un articolo dettagliato di 500-600 parole sul tema '{topic}' "
        f"in lingua '{language}', adatto per un blog di salute e benessere. "
        "Ottimizza per SEO e dividi in paragrafi."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un esperto di contenuti SEO e salute."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    return response["choices"][0]["message"]["content"]


def insert_product_boxes(content, links, max_boxes=2):
    """
    Inserisce i Product Box HTML in posizioni strategiche nel contenuto.
    """
    from .product_box_generator import generate_product_box as generate_product_box_html
    paragraphs = content.split("\n\n")
    inserted = 0
    for i in range(len(paragraphs)):
        if inserted < max_boxes and i % 3 == 0 and links:
            link = links.pop(0)
            box_html = generate_product_box_html(
                title=link.get('nome', 'Scopri di più'),
                description=link.get('description', ''),
                image_url=link.get('image_url', ''),
                affiliate_link=link.get('url', '#')
            )
            paragraphs[i] += "\n\n" + box_html
            inserted += 1
    return "\n\n".join(paragraphs)

