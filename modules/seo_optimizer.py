import re

def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Calcola un tempo di lettura approssimativo in minuti,
    contando le parole e dividendo per la velocità media.
    """
    # Conta tutte le parole (sequenze di lettere/cifre)
    word_count = len(re.findall(r'\w+', text))
    # Calcola i minuti, almeno 1
    minutes = max(1, int(word_count / words_per_minute))
    return minutes


def apply_seo_structure(article_text, keyword):
    title = f"{keyword.title()} - Guida Completa"
    meta_description = article_text[:150].replace('\n', ' ')
    return {
        "title": title,
        "meta_description": meta_description,
        "slug": keyword.replace(" ", "-").lower(),
        "content": article_text
    }
