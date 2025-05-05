#!/usr/bin/env python3
import argparse
import csv
import json
import os

from db import insert_metrics

def load_csv_count(path):
    """Carica un CSV con header e conta le righe (esclude header)."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # salta header
        next(reader, None)
        return sum(1 for _ in reader)

def load_revenue(path):
    """Carica CSV con colonne [titolo_articolo, n_conversioni, guadagno_totale] 
       e somma la colonna guadagno_totale."""
    total = 0.0
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += float(row['guadagno_totale'])
    return total

def main():
    parser = argparse.ArgumentParser(
        description="Esegue l'ingestion delle metriche e salva in DB + JSON"
    )
    parser.add_argument(
        "--clicks-path", required=True,
        help="Percorso a clicks.csv (header + una riga per click)"
    )
    parser.add_argument(
        "--conversions-path", required=True,
        help="Percorso a conversions.csv (header + una riga per conversione)"
    )
    parser.add_argument(
        "--revenue-path", required=True,
        help="Percorso a conversion_report.csv (con colonna guadagno_totale)"
    )
    args = parser.parse_args()

    # 1) Leggi i dati
    clicks      = load_csv_count(args.clicks_path)
    conversions = load_csv_count(args.conversions_path)
    revenue     = load_revenue(args.revenue_path)

    metrics = {
        "clicks":      clicks,
        "conversions": conversions,
        "revenue":     revenue
    }

    # 2) Inserisci in DB (stub)
    insert_metrics(**metrics)
    print(f"🔔 insert_metrics stub called with: {metrics}")

    # 3) Scrivi l'output JSON
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "metrics.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"✅ Metrics saved to {out_path}: {metrics}")

if __name__ == "__main__":
    main()
