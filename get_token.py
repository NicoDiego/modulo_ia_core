import os
import sys
import logging
import requests
from config.settings_loader import settings, BASE_DIR, LOG_DIR

# Configurazione logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'token_gen.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Parametri di autenticazione (preferisce ENV vars)
SITE_URL = settings.get('wp_site_url')
USERNAME = os.getenv('WP_USER')
PASSWORD = os.getenv('WP_PASS')

TOKEN_PATH = os.path.join(BASE_DIR, 'in.save')

def get_jwt_token():
    """
    Richiede un JWT token a WordPress e lo salva in in.save.
    """
    url = f"{SITE_URL}/wp-json/jwt-auth/v1/token"
    payload = {"username": USERNAME, "password": PASSWORD}
    try:
        resp = requests.post(url, data=payload, timeout=10)
        resp.raise_for_status()
        token = resp.json().get('token')
        if not token:
            raise ValueError(f"Tentativo fallito, risposta: {resp.text}")

        with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
            f.write(token)

        logging.info("Token JWT salvato con successo")
        return token

    except Exception as e:
        logging.error(f"Errore durante get_jwt_token: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    tok = get_jwt_token()
    print(f"✅ Token ottenuto e salvato in: {TOKEN_PATH}")
