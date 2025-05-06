# modules/metrics_loader.py
import os
import json
from config.settings_loader import BASE_DIR

METRICS_PATH = os.path.join(BASE_DIR, 'modules', 'output', 'metrics.json')

def load_metrics() -> dict:
    """
    Ritorna il dict di metrics da metrics.json o {} se non esiste.
    """
    if not os.path.exists(METRICS_PATH):
        return {}
    with open(METRICS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
