#!/usr/bin/env python3
# flake8: noqa
# modules/metrics_ingestion.py

import os
import csv
import json
from config.settings_loader import BASE_DIR

def _safe_int(val, default=999):
    try:
        return int(val)
    except Exception:
        return default

def _safe_float(val, default=0.0):
    try:
        return float(val)
    except Exception:
        return default

def ingest_metrics(conversions_path: str, output_path: str):
    """
    Legge un CSV di conversioni con colonne slug,pos,ctr,revenue
    e scrive output_path (metrics.json) mappando per slug.
    Se il valore di pos/ctr/revenue non è convertibile, usa default.
    """
    metrics = {}

    with open(conversions_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []

        slug_key = "slug" if "slug" in fields else fields[0]
        pos_key  = "pos"  if "pos"  in fields else (fields[1] if len(fields)>1 else slug_key)
        ctr_key  = "ctr"  if "ctr"  in fields else (fields[2] if len(fields)>2 else "")
        rev_key  = "revenue" if "revenue" in fields else (fields[3] if len(fields)>3 else "")

        for row in reader:
            slug = row.get(slug_key, "").strip()
            if not slug:
                continue

            metrics[slug] = {
                'position': _safe_int(row.get(pos_key, None), 999),
                'ctr':      _safe_float(row.get(ctr_key, None), 0.0),
                'revenue':  _safe_float(row.get(rev_key, None), 0.0)
            }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved metrics for {len(metrics)} articles to {output_path}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Ingest per-article SEO metrics")
    parser.add_argument(
        '--conversions-path',
        required=True,
        help="CSV con colonne slug,pos,ctr,revenue (o simili)"
    )
    args = parser.parse_args()

    out = os.path.join(BASE_DIR, 'modules', 'output', 'metrics.json')
    ingest_metrics(args.conversions_path, out)
