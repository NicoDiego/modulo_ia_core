#!/usr/bin/env python3
# File: modules/metrics_ingestion.py

import argparse
import csv
import json
import os
from db import insert_metrics  # il tuo stub in db.py


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ingest metrics from CSV and persist them"
    )
    parser.add_argument(
        "--clicks-path",
        required=True,
        help="Percorso al file CSV con i click",
    )
    parser.add_argument(
        "--conversions-path",
        required=True,
        help="Percorso al file CSV con le conversioni",
    )
    parser.add_argument(
        "--revenue-path",
        required=True,
        help="Percorso al file CSV con i ricavi",
    )
    return parser.parse_args()


def count_rows(path):
    """Conta quante righe (escluse eventuali intestazioni) ci sono in un CSV."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        return sum(1 for _ in reader)


def sum_revenue(path):
    """Somma i valori della colonna 'revenue' (o ultima colonna) di un CSV."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        key = "revenue" if "revenue" in reader.fieldnames else reader.fieldnames[-1]
        return sum(float(row.get(key, 0)) for row in reader)


def main():
    args = parse_args()

    clicks = count_rows(args.clicks_path)
    conversions = count_rows(args.conversions_path)
    revenue = sum_revenue(args.revenue_path)

    # 1) Invia i dati al DB (stub)
    insert_metrics(clicks=clicks, conversions=conversions, revenue=revenue)

    # 2) Scrive su disco un JSON di output per il workflow
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "metrics.json")

    metrics = {
        "clicks":      clicks,
        "conversions": conversions,
        "revenue":     revenue,
    }

    with open(out_path, "w") as f:
        json.dump(metrics, f)

    print(f"✅ Metrics saved to {out_path}: {metrics}")


if __name__ == "__main__":
    main()

