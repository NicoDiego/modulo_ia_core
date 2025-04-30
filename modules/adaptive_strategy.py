
import csv
from collections import Counter

def load_conversion_report(path='data/conversion_report.csv'):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_top_keywords_from_report(report, top_n=5):
    # Estrapola parole chiave più ricorrenti nei titoli degli articoli con più conversioni
    weighted_words = []
    for row in report:
        title = row['titolo_articolo']
        conversions = int(row.get('n_conversioni', 0))
        words = [w.lower() for w in title.split() if len(w) > 3]
        weighted_words.extend(words * conversions)

    common = Counter(weighted_words).most_common(top_n)
    return [word for word, _ in common]

def adjust_generation_params():
    report = load_conversion_report()
    keywords = get_top_keywords_from_report(report)
    print(f"🔁 Parole chiave più performanti: {keywords}")
    return keywords
