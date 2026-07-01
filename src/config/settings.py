import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Cargar de inmediato las variables del archivo .env
load_dotenv()

# Ubicar la raíz del proyecto (Real-Estate-Scraper-Pro) subiendo 3 niveles desde este archivo
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Rutas exactas a las carpetas principales del sistema
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
REPORTS_DIR = EXPORTS_DIR / "reports"
ASSETS_DIR = EXPORTS_DIR / "assets"

# Ruta absoluta hacia el archivo físico de la base de datos SQLite
DB_PATH = DATA_DIR / "market_intel.db"

# Configuración de correo electrónico para el módulo de notificaciones
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
# Variables dinámicas para permitir cualquier servidor de correo del mercado
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def verify_project_folders():
    """Garantiza que las carpetas de almacenamiento existan antes de que el bot trabaje."""
    for folder in [DATA_DIR, REPORTS_DIR, ASSETS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

def get_excel_filename(city=None):
    fecha = datetime.now().strftime("%Y-%m-%d")

    if city:
        safe_city = city.lower().replace(" ", "_")
        return f"reporte_{safe_city}_{fecha}.xlsx"

    return f"reporte_global_{fecha}.xlsx"