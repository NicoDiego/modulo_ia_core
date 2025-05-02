import os
import sys
import json
import logging

from config.settings_loader import settings, BASE_DIR, DATA_DIR, OUTPUT_DIR, LOG_DIR
from get_token import get_jwt_token
from modules.trend_hunter import get_trending_keywords, SUPPORTED_LANGS
from modules.adaptive_strategy import adjust_generation_params
from modules.content_generator import generate_article, insert_product_boxes
from modules.translator import translate_text
from modules.seo_optimizer import apply_seo_structure, calculate_reading_time
from modules.affiliate_api.loader import load_affiliate_links
from modules.wp_publisher import publish_to_wp
from modules.publish_manager import can_publish
from modules.logger import log
from modules.seo_refiner import enhance_article
from modules.conversion_analyzer import load_clicks_map, analyze_conversions, print_report
from modules.related_articles import get_all_articles, pick_related_articles

# Configurazione logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'generazione.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def main():
    try:
        # 1) Ottieni e aggiorna il token WP
        token = get_jwt_token()
        settings['wp_token'] = token

        # 2) Carica categorie dinamiche
        cat_file = os.path.join(BASE_DIR, 'categorie_dinamiche.json')
        with open(cat_file, 'r', encoding='utf-8') as f:
            categorie_map = json.load(f)

        # 3) Analisi conversioni
        clicks_map = load_clicks_map(os.path.join(DATA_DIR, 'clicks.csv'))
        stats      = analyze_conversions(clicks_map, os.path.join(DATA_DIR, 'conversions.csv'))
        print_report(stats)

        # 4) Trend hunting + adaptive keywords
        default_lang = settings.get('languages', ['it'])[0]
        lang_conf    = SUPPORTED_LANGS.get(default_lang, {'lang': default_lang, 'geo': default_lang})
        trending     = get_trending_keywords(lang=lang_conf['lang'], geo=lang_conf['geo'], limit=5)
        adaptive     = adjust_generation_params()
        keywords     = trending + [kw for kw in adaptive if kw not in trending]

        # 5) Affiliazioni
        affiliate_links = load_affiliate_links(keywords, per_source=2)
        auto_pub        = settings.get('auto_publish', False)

        # 6) Loop di generazione e pubblicazione
        for kw in keywords:
            # Genera contenuto base e box affiliati
            base     = generate_article(kw, language='it')
            with_boxes = insert_product_boxes(base, affiliate_links.copy(), max_boxes=2)

            # SEO e migliorie
            seo       = apply_seo_structure(with_boxes, kw)
            enhanced  = enhance_article(seo['content'], seo['title'], kw)
            seo.update(enhanced)
            seo['content'] = f"⏱️ Tempo di lettura: {calculate_reading_time(seo['content'])} minuti\n\n" + seo['content']

            categoria = categorie_map.get(kw.lower(), 'Generale')
            logging.info(f"Articolo IT creato: {seo['title']} – Categoria: {categoria}")

            # Salvataggio locale con backup
            filename = f"{seo['slug']}_it.md"
            safe_write(os.path.join(OUTPUT_DIR, filename), seo['content'])

            # Pubblicazione IT
            if can_publish('it', categoria):
                if auto_pub:
                    publish_to_wp(
                        title=seo['title'],
                        content=seo['content'],
                        slug=seo['slug'],
                        lang='it',
                        category=categoria,
                        meta_title=seo.get('meta_title'),
                        meta_description=seo.get('meta_description')
                    )
                    log(f"Pubblicato IT: {seo['title']}")
                else:
                    print(f"🔖 Pronto per pubblicazione manuale: {seo['title']}")
            else:
                print(f"⏸️ Bozza IT: {seo['title']}")

            # Traduzioni e pubblicazione multilingua
            for lang in settings.get('languages', []):
                if lang == 'it':
                    continue

                trad = translate_text(base, lang)
                related = pick_related_articles(get_all_articles(lang), exclude_slug=seo['slug'])
                if related:
                    blocco = "\n\n<hr><h3>Articoli Correlati</h3><ul>"
                    blocco += "".join(f'<li><a href="{a["link"]}">{a["title"]}</a></li>' for a in related)
                    blocco += "</ul>\n\n"
                    trad += blocco

                # Salvo e (opzionalmente) pubblico
                safe_write(os.path.join(OUTPUT_DIR, f"{seo['slug']}_{lang}.md"), trad)
                if auto_pub and can_publish(lang, categoria):
                    publish_to_wp(
                        title=seo['title'],
                        content=trad,
                        slug=seo['slug'],
                        lang=lang,
                        category=categoria,
                        meta_title=seo.get('meta_title'),
                        meta_description=seo.get('meta_description')
                    )
                    log(f"Pubblicato {lang.upper()}: {seo['title']}")

    except Exception as e:
        logging.exception("Errore nella pipeline run_ai")
        sys.exit(1)

if __name__ == '__main__':
    main()


