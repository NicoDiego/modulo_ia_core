
from pytrends.request import TrendReq

def get_trending_keywords(lang="en", geo="US", category="health", limit=5):
    pytrends = TrendReq(hl=lang, tz=360)
    pytrends.build_payload(kw_list=["salute", "vitamina", "integratori"], geo=geo, cat=0)
    
    related = pytrends.related_queries()
    keywords = []

    for key in related:
        rising = related[key].get("rising")
        if rising is not None:
            for i in rising.head(limit).itertuples():
                keywords.append(i.query)

    return keywords


# Lingue supportate per il progetto IA multilingua

SUPPORTED_LANGS = {
    "it": {"lang": "it", "geo": "IT"},
    "en": {"lang": "en", "geo": "US"},
    "es": {"lang": "es", "geo": "ES"},
    "fr": {"lang": "fr", "geo": "FR"},
    "de": {"lang": "de", "geo": "DE"},
    "pt": {"lang": "pt", "geo": "BR"},
    "nl": {"lang": "nl", "geo": "NL"},
    "sv": {"lang": "sv", "geo": "SE"},
    "no": {"lang": "no", "geo": "NO"},
    "da": {"lang": "da", "geo": "DK"},
    "pl": {"lang": "pl", "geo": "PL"},
    "ro": {"lang": "ro", "geo": "RO"},
    "cs": {"lang": "cs", "geo": "CZ"},
    "sk": {"lang": "sk", "geo": "SK"},
    "hu": {"lang": "hu", "geo": "HU"},
    "el": {"lang": "el", "geo": "GR"}
}
