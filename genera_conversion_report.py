import os
from config.settings_loader import DATA_DIR
from modules.conversion_analyzer import load_clicks_map, analyze_conversions, print_report, save_report
from modules.content_generator import safe_write

if __name__ == '__main__':
    # Percorsi assoluti
    clicks_path = os.path.join(DATA_DIR, 'clicks.csv')
    conv_path   = os.path.join(DATA_DIR, 'conversions.csv')
    report_path = os.path.join(DATA_DIR, 'conversion_report.csv')

    # 1) Carica dati e calcola statistiche
    clicks = load_clicks_map(clicks_path)
    stats  = analyze_conversions(clicks, conv_path)
    print_report(stats)

    # 2) Salva report (safe_write crea backup se esiste già)
    csv_content = save_report(stats)  
    safe_write(report_path, csv_content)

    print(f"\n✅ Report generato in: {report_path}")
