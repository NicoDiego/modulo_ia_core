
import csv
from collections import defaultdict

def load_clicks_map(clicks_path):
    click_map = {}
    with open(clicks_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            click_map[row['click_id']] = row
    return click_map

def analyze_conversions(click_map, conversions_path):
    stats = defaultdict(lambda: {'n_conversioni': 0, 'guadagno_totale': 0.0})
    with open(conversions_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            click_id = row['click_id']
            amount = float(row['amount'])
            if click_id in click_map:
                titolo = click_map[click_id]['titolo_articolo']
                stats[titolo]['n_conversioni'] += 1
                stats[titolo]['guadagno_totale'] += amount
    return [{'titolo_articolo': k,
             'n_conversioni': v['n_conversioni'],
             'guadagno_totale': round(v['guadagno_totale'], 2)} for k, v in stats.items()]

def print_report(stats):
    print("\n=== Report Conversioni per Articolo ===")
    for row in stats:
        print(f"{row['titolo_articolo']}: {row['n_conversioni']} conversioni - €{row['guadagno_totale']}")

def save_report(stats, path='data/conversion_report.csv'):
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['titolo_articolo', 'n_conversioni', 'guadagno_totale']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for stat in stats:
            writer.writerow(stat)
