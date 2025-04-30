# /modules/product_box_generator.py

def generate_product_box(title, description, image_url, affiliate_link):
    """
    Crea un box HTML accattivante per promuovere un prodotto.
    """
    return f'''
<div style="border:1px solid #eee; border-radius:12px; padding:20px; background:#f9f9f9; text-align:center; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin:20px 0;">
    <h3 style="margin-bottom:10px; color:#333;">{title}</h3>
    <img src="{image_url}" alt="{title}" style="width:200px; border-radius:8px; margin-bottom:15px;">
    <p style="color:#555; font-size:16px; margin-bottom:20px;">{description}</p>
    <a href="{affiliate_link}" target="_blank" style="background:#ff6600; color:white; padding:12px 24px; border-radius:24px; font-size:18px; text-decoration:none; box-shadow: 0px 2px 6px rgba(0,0,0,0.2);">Scopri l'Offerta</a>
</div>
'''

def generate_product_box(title, description, image_url, affiliate_link):
    """
    Genera un box HTML elegante per promuovere un prodotto.
    """
    return f"""
    <div style="border: 2px solid #FFA500; padding: 20px; border-radius: 12px; background: #FFF8F0; margin-top: 30px; margin-bottom: 30px;">
        <h3 style="text-align: center; color: #FF5722;">{title}</h3>
        <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 15px;">
            <img src="{image_url}" alt="Prodotto Consigliato" style="max-width: 150px; border-radius: 8px;">
            <div style="max-width: 400px;">
                <p style="text-align: center; font-size: 18px; color: #555;">{description}</p>
                <div style="text-align: center; margin-top: 15px;">
                    <a href="{affiliate_link}" target="_blank" style="background-color: #FF5722; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; text-decoration: none;">
                        👉 Scopri l'Offerta
                    </a>
                </div>
            </div>
        </div>
    </div>
    """
