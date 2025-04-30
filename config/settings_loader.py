import os
import json
from dotenv import load_dotenv

# 1. BASE_DIR: cartella root del progetto (due livelli sopra questo file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Caricamento variabili da .env (se esiste in BASE_DIR)
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 3. Costanti per percorsi assoluti
DATA_DIR    = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR  = os.path.join(BASE_DIR, 'output')
LOG_DIR     = os.path.join(BASE_DIR, 'logs')
CONFIG_DIR  = os.path.join(BASE_DIR, 'config')

# 4. Percorso al file di configurazione JSON
SETTINGS_PATH = os.path.join(CONFIG_DIR, 'settings.json')

def load_settings():
    """
    Carica settings.json e applica override dalle variabili d'ambiente.
    Ritorna un dict con TUTTE le impostazioni del progetto.
    """
    # 4.1 Lettura JSON
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # 4.2 Override con ENV VAR (se presenti)
    # (i nomi evalgono se hai aggiunto .env.example con gli stessi nomi)
    cfg['openai_api_key']   = os.getenv('OPENAI_API_KEY',   cfg.get('openai_api_key'))
    cfg['pixabay_api_key']  = os.getenv('PIXABAY_API_KEY',  cfg.get('pixabay_api_key'))
    cfg['wp_site_url']      = os.getenv('WP_SITE_URL',      cfg.get('wp_site_url'))
    cfg['wp_token']         = os.getenv('WP_TOKEN',         cfg.get('wp_token'))

    return cfg

# 5. Oggetto globale di configurazione, importabile da tutti i moduli
settings = load_settings()
