#!/usr/bin/env python3
import os, sys

# Assicura che la cartella root sia nel PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import argparse
from modules.metrics_loader import load_metrics

def load_first_json(path):
    """
    Legge un file che contiene uno o più JSON concatenati,
    ritorna solo il primo oggetto decodificato.
    """
    text = open(path, 'r', encoding='utf-8').read()
    text = text.lstrip()
    decoder = json.JSONDecoder()
    obj, idx = decoder.raw_decode(text)
    return obj

def evaluate(old_metrics_path: str):
    """
    Confronta posizione vecchia vs nuova per ogni slug.
    """
    # carica solo il primo JSON, ignora eventuale “extra data”
    old = load_first_json(old_metrics_path)

    new = load_metrics()
    for slug, new_data in new.items():
        old_pos = old.get(slug, {}).get('position', new_data['position'])
        delta = old_pos - new_data['position']
        print(f"{slug}: Δposition = {delta:+}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Valuta miglioramenti posizionali dopo revisione"
    )
    parser.add_argument(
        "--old", required=True,
        help="Path al JSON delle vecchie metrics (es. old_metrics.json)"
    )
    args = parser.parse_args()
    evaluate(args.old)
