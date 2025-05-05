#!/usr/bin/env python3
# File: scripts/evaluate_model.py

import argparse
import json
import os

def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate model performance and emit metrics for GitHub Actions"
    )
    parser.add_argument(
        "--model-dir",
        required=True,
        help="Directory where the trained model and metrics.json are stored"
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Directory containing the processed data for evaluation"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    metrics_path = os.path.join(args.model_dir, "metrics.json")

    # Carica il file JSON prodotto dallo script di training
    with open(metrics_path, "r") as f:
        metrics = json.load(f)

    # Estrai le metriche chiave, usando 0 come default
    accuracy = metrics.get("accuracy", 0)
    previous_accuracy = metrics.get("previous_accuracy", 0)

    # Stampa in console per i log e imposta gli output per GitHub Actions
    print(f"✅ Current accuracy: {accuracy}")
    print(f"ℹ️ Previous accuracy: {previous_accuracy}")
    print(f"::set-output name=accuracy::{accuracy}")
    print(f"::set-output name=previous_accuracy::{previous_accuracy}")

if __name__ == "__main__":
    main()
