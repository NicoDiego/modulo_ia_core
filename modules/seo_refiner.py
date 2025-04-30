import re

def estimate_reading_time(text):
    """Stima il tempo di lettura basato su 200 parole al minuto."""
    words = len(text.split())
    minutes = max(1, int(words / 200))
    return minutes

def improve_readability(text):
    """Migliora leggibilità dividendo paragrafi troppo lunghi."""
    paragraphs = text.split("\n\n")
    new_paragraphs = []
    for p in paragraphs:
        if len(p.split()) > 100:
            # Se il paragrafo è troppo lungo, lo spezziamo
            sentences = re.split(r'(?<=[.!?]) +', p)
            mid = len(sentences) // 2
            new_paragraphs.append(' '.join(sentences[:mid]))
            new_paragraphs.append(' '.join(sentences[mid:]))
        else:
            new_paragraphs.append(p)
    return "\n\n".join(new_paragraphs)

def generate_meta_title(title, keyword=None):
    """Crea un Meta Title SEO-friendly."""
    if keyword and keyword.lower() not in title.lower():
        return f"{title} - {keyword.capitalize()}"
    return title

def generate_meta_description(content, keyword=None):
    """Genera una meta description prendendo l'inizio dell'articolo."""
    sentences = re.split(r'(?<=[.!?]) +', content.strip())
    description = ""
    for sentence in sentences:
        if len(description) + len(sentence) < 160:
            description += sentence + " "
        else:
            break
    if keyword and keyword.lower() not in description.lower():
        description = keyword.capitalize() + ": " + description
    return description.strip()

def enhance_article(text, title, keyword=None):
    """Applica tutte le migliorie SEO: tempo lettura, leggibilità, ecc."""
    improved = improve_readability(text)
    minutes = estimate_reading_time(improved)
    intro = f"🕒 Tempo di lettura: circa {minutes} minuti.\n\n"
    full_content = intro + improved
    meta_title = generate_meta_title(title, keyword)
    meta_description = generate_meta_description(improved, keyword)
    return {
        "content": full_content,
        "meta_title": meta_title,
        "meta_description": meta_description
    }
