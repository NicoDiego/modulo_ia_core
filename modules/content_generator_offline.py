
def generate_article(topic, language="it"):
    return f"""
# Titolo dell'articolo su '{topic}' [{language.upper()}]

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.

- ✅ Simulazione IA
- 🌐 Lingua: {language}
- 🔍 Keyword: {topic}

Test di generazione articolo senza chiamate API.

"""
