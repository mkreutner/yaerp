# 3. Première Implémentation

## 3.1. La première étape concrète

Pour ne pas perdre de temps, nous commencerons par un script sur un seul concurrent et uen dixaines de produits clés.

Voici une structure de base en Python pour un premier essai.

## 3.1.1. Le Script de base (Python + Playwright)

Ce script se rend sur une page, attend que le prix s'affiche, le récupère et le nettoie.

```Python
iimport asyncio
import csv
import os
import random  # Pour les délais aléatoires
from datetime import datetime
from playwright.async_api import async_playwright

# --- CONFIGURATION ---
TARGETS = [
    {
        "competitor_name": "IPLN",
        "products_list": [
           {
               "product_name": "PANASONIC HYBRIDE LUMIX S5 II",
               "url": "https://ipln.fr/appareil-photo-hybride/9020-4900-panasonic-hybride-lumix-s5-ii",
               "selectors": [".regular-price", ".current-price"]
           },
        ],
    },
    {
        "competitor_name": "MNPhoto-Video",
        "products_list": [
            {
                "product_name": "PANASONIC HYBRIDE LUMIX S5 II",
                "url": "https://www.mnphotovideo.com/panasonic-lumix-s5-ii-p-58000.html",
                "selectors": ["#responsive_line_price", ".ficheproduct_prix_produit"]
            },
        ],
    }
]

def clean_price(text):
    if not text or "trouvé" in text: return None
    try:
        # Nettoyage pour garder uniquement chiffres, virgules et points
        clean = "".join(c for c in text if c.isdigit() or c in (',', '.'))
        return float(clean.replace(',', '.'))
    except: return text

def get_dynamic_filename(competitor_name):
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{date_str}_{competitor_name.upper().replace(' ', '_')}_price.csv"

async def save_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Produit', 'Sélecteur', 'Valeur', 'URL'])
        writer.writerow(data)

async def run_scraping(competitors_data):
    async with async_playwright() as p:
        # Dossier de session pour conserver les cookies Cloudflare
        user_data_dir = os.path.join(os.getcwd(), "browser_session")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False, # Garder visible pour Cloudflare
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        for competitor in competitors_data:
            filename = get_dynamic_filename(competitor["competitor_name"])
            print(f"\n--- Compétiteur : {competitor['competitor_name']} ---")

            for item in competitor["products_list"]:
                page = await context.new_page()
                
                # --- INJECTION MANUELLE STEALTH (Remplace la lib en erreur) ---
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                """)
                
                print(f"  > Analyse : {item['product_name']}")
                
                try:
                    # Délai aléatoire avant d'accéder à la page (entre 2 et 5 secondes)
                    await asyncio.sleep(random.uniform(2, 5))
                    
                    await page.goto(item['url'], wait_until="domcontentloaded", timeout=60000)
                    
                    # Pause pour laisser Cloudflare vérifier
                    await asyncio.sleep(5)

                    for selector in item['selectors']:
                        try:
                            # Attente du sélecteur
                            element = await page.wait_for_selector(selector, timeout=10000)
                            raw_text = await element.inner_text()
                            value = clean_price(raw_text)
                            
                            await save_to_csv(filename, [
                                datetime.now().strftime("%H:%M:%S"),
                                item['product_name'], selector, value, item['url']
                            ])
                            print(f"    [OK] {selector}: {value}")
                        except:
                            print(f"    [!] Absent : {selector}")
                
                except Exception as e:
                    print(f"    [!] Erreur sur l'URL : {e}")
                
                finally:
                    await page.close()
                    # Pause après fermeture pour la RAM
                    await asyncio.sleep(random.uniform(3, 6))

        await context.close()

if __name__ == "__main__":
    asyncio.run(run_scraping(TARGETS))
```