import openai
import re

def generate_article(topic, affiliate_links=None, max_tokens=1500, keyword_density=None, language="it"):
    """
    Scrive un articolo SEO‐ottimizzato sul topic, con eventuali box affiliate.
    Ora accetta max_tokens e keyword_density.
    """
    prompt = (
        f"Scrivi un articolo dettagliato di 500-600 parole sul tema '{topic}' "
        f"in lingua '{language}', adatto per un blog di salute e benessere. "
        "Ottimizza per SEO e dividi in paragrafi."
    )
    # (potresti integrare keyword_density nel prompt se vuoi)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un esperto di contenuti SEO e salute."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )

    return response["choices"][0]["message"]["content"]


def insert_product_boxes(content, links, max_boxes=2):
    """
    Inserisce box HTML di prodotti in content.
    """
    from .product_box_generator import generate_product_box as gen_box

    paragraphs = content.split("\n\n")
    inserted = 0
    for i in range(len(paragraphs)):
        if inserted < max_boxes and links and i % 3 == 0:
            link = links.pop(0)
            box = gen_box(
                title=link.get("title"),
                description=link.get("description"),
                image_url=link.get("image_url"),
                affiliate_link=link.get("url")
            )
            paragraphs[i] += "\n\n" + box
            inserted += 1
    return "\n\n".join(paragraphs)


def calculate_reading_time(content):
    """
    Calcola tempo di lettura approssimato (200 parole/min).
    """
    words = re.findall(r"\w+", content)
    return max(1, int(len(words) / 200))


