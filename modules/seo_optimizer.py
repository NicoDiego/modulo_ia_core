def apply_seo_structure(article_text, keyword):
    title = f"{keyword.title()} - Guida Completa"
    meta_description = article_text[:150].replace('\n', ' ')
    return {
        "title": title,
        "meta_description": meta_description,
        "slug": keyword.replace(" ", "-").lower(),
        "content": article_text
    }
