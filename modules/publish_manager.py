import os
import json
from datetime import datetime
from config.settings_loader import settings

# Path al file di persistenza dei contatori
COUNTERS_PATH = os.path.join("data", "counters.json")

# Carica lo stato dei contatori, azzera se cambio data
def _load_counters():
    if os.path.exists(COUNTERS_PATH):
        with open(COUNTERS_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"last_reset": "", "counters": {}}

    today = datetime.now().strftime("%Y-%m-%d")
    if state.get("last_reset") != today:
        # Reset giornaliero
        state = {"last_reset": today, "counters": {}}
        _save_counters(state)
    return state

# Salva lo stato dei contatori su file
def _save_counters(state):
    os.makedirs(os.path.dirname(COUNTERS_PATH), exist_ok=True)
    with open(COUNTERS_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# Controlla se è possibile pubblicare, usando contatori persistenti
def can_publish(lang, category):
    ps = settings.get("publish_settings", {})
    default_mode = ps.get("default_mode", "publish")
    max_articles_global = ps.get("max_articles_per_day", 9999)

    lang_settings = ps.get("per_language", {}).get(lang, {})
    mode = lang_settings.get("mode", default_mode)
    max_articles_lang = lang_settings.get("max_articles", max_articles_global)
    per_category_limits = lang_settings.get("per_category", {})

    # Carica contatori
    state = _load_counters()
    counters = state["counters"]

    lang_key = f"{lang}_total"
    cat_key = f"{lang}_{category}"

    counters.setdefault(lang_key, 0)
    counters.setdefault(cat_key, 0)

    # Se in modalità draft forzato
    if mode == "draft":
        return False
    # Limite globale lingua
    if counters[lang_key] >= max_articles_lang:
        return False
    # Limiti per categoria
    if category in per_category_limits:
        if counters[cat_key] >= per_category_limits[category]:
            return False
    return True

# Aggiorna i contatori e li persiste
def mark_published(lang, category):
    state = _load_counters()
    counters = state["counters"]

    lang_key = f"{lang}_total"
    cat_key = f"{lang}_{category}"

    counters[lang_key] = counters.get(lang_key, 0) + 1
    counters[cat_key] = counters.get(cat_key, 0) + 1

    _save_counters(state)

