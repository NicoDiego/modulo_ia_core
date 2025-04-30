
import csv
import os

def generate_dashboard_html(report_path='data/conversion_report.csv', output_path='output/dashboard.html'):
    # read report
    rows = []
    with open(report_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    # build html
    html = ['<html><head><title>Conversion Dashboard</title><style>table{width:80%;border-collapse:collapse;}td,th{border:1px solid #ccc;padding:8px;text-align:left;}</style></head><body>']
    html.append('<h1>Conversion Dashboard</h1>')
    html.append('<table><tr><th>Articolo</th><th>Conversioni</th><th>Guadagno (€)</th></tr>')
    for r in rows:
        html.append(f"<tr><td>{r['titolo_articolo']}</td><td>{r['n_conversioni']}</td><td>{r['guadagno_totale']}</td></tr>")
    html.append('</table></body></html>')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(html))
    print(f"Dashboard generated at {output_path}")

if __name__ == '__main__':
    generate_dashboard_html()
