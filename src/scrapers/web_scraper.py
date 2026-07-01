import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,en-US;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


def configurar_options_camufladas():
    chrome_options = Options()

    # Headless moderno
    chrome_options.add_argument("--headless=new")

    # Anti-detección básica
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Identidad realista
    chrome_options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    return chrome_options


def crear_archivo_auditoria(html):
    try:
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("[AUDITORÍA] HTML guardado en debug_page.html")
    except Exception as e:
        print(f"[ERROR] Auditoría falló: {e}")


def fetch_html_content(url):
    driver = None

    try:
        options = configurar_options_camufladas()
        driver = webdriver.Chrome(options=options)

        print(f"[SCRAPER] Abriendo: {url}")
        driver.get(url)

        # ✅ ESPERA INTELIGENTE (CLAVE)
        print("[SCRAPER] Esperando carga real de listings...")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='listing-card']"))
        )

        # extra buffer para JS pesado
        time.sleep(2)

        html = driver.page_source

        crear_archivo_auditoria(html)

        return html

    except Exception as e:
        print(f"[ERROR CRÍTICO SCRAPER] {e}")
        return None

    finally:
        if driver:
            driver.quit()