# Raccoglie e carica su DB (Postgres/BigQuery)
from db import insert_metrics
import csv
import os


def load_metrics(table: str, path: str):
    """Carica metriche da CSV su tabella specificata."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File non trovato: {path}")
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert_metrics(table, row)


def load_clicks(path: str):
    load_metrics('clicks', path)


def load_conversions(path: str):
    load_metrics('conversions', path)


def load_revenue(path: str):
    load_metrics('revenue', path)


if __name__ == '__main__':
    # Esegui ingestion per tutte le metriche
    load_clicks('data/clicks.csv')
    load_conversions('data/conversions.csv')
    load_revenue('data/revenue.csv')