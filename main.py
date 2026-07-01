import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from database_mod.db_manager import create_tables, clear_database
from database_mod.db_manager import get_connection
from parsers.html_parser import parse_listings_html
from processors.excel_reporter import generate_market_report
from visualizers.chart_generator import generate_listings_chart
from scrapers.web_scraper import fetch_html_content
from tools.file_handler import clear_generated_reports
from tools.email_notifier import send_market_report_email
from tools.email_notifier import send_full_report_email
from visualizers.chart_generator import generate_market_chart
from tools.location_parser import resolve_zumper_city, build_zumper_url

# 🔥 NUEVO: guardar última ciudad
last_city = None


TEXTS = {
    "es": {
        "title": "============================================================\n"
                 "   SISTEMA UNIVERSAL DE AUDITORÍA INMOBILIARIA (UACS)\n"
                 "============================================================",
        "opt1": "[1] Iniciar Escaneo de Datos (Descargar y Guardar en Base de Datos)",
        "opt2": "[2] Generar Reportes Ejecutivos (Crear Excel y Gráfico PNG)",
        "opt3": "[3] Limpiar Archivos Generados (Borrar Excel y PNG del disco)",
        "opt4": "[4] Vaciar Base de Datos (Borrar todo el historial local)",
        "opt5": "[5] Enviar Reportes por Correo (Despacho Electrónico TLS)",
        "opt6": "[6] Enviar TODOS los reportes (todas las ciudades)",
        "opt0": "[0] Salir del Sistema",
        "select_opt": "\nSeleccione una opción: ",
        "invalid_opt": "[ERROR] Opción inválida. Intente de nuevo.",
        "ask_city": "Ingrese la ciudad de USA a escanear (Ej. miami, detroit, new york): ",
        "goodbye": "SISTEMA CERRADO. ¡HASTA LUEGO!"
    },

    "en": {
        "title": "============================================================\n"
                 "   UNIVERSAL AUDIT CONTROL SYSTEM (UACS)\n"
                 "============================================================",
        "opt1": "[1] Start Data Scanning (Download & Save to Database)",
        "opt2": "[2] Generate Executive Reports (Create Excel & PNG Chart)",
        "opt3": "[3] Clear Generated Files (Delete Excel & PNG from disk)",
        "opt4": "[4] Empty Database (Delete all local history)",
        "opt5": "[5] Send Reports via Email (TLS Electronic Dispatch)",
        "opt6": "[6] Send ALL reports (all cities)",
        "opt0": "[0] Exit System",
        "select_opt": "\nSelect an option: ",
        "invalid_opt": "[ERROR] Invalid option. Please try again.",
        "ask_city": "Enter the US city to scan (e.g., miami, detroit, new york): ",
        "goodbye": "SYSTEM CLOSED. GOODBYE!"
    }
}


def get_cities_from_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT city
            FROM properties
            WHERE city IS NOT NULL
            ORDER BY city
        """)

        cities = [row[0] for row in cursor.fetchall()]
        conn.close()

        return cities

    except Exception as e:
        print(f"[ERROR] No se pudieron obtener ciudades: {e}")
        return []

def init_system_environment():
    print("[INIT] Verificando infraestructura local de SQLite...")
    try:
        create_tables()
        print("[INIT] Base de datos SQLite verificada y lista para operar.")
    except Exception as e:
        print(f"[CRITICAL ERROR] Fallo al inicializar la base de datos: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_system_environment()

    print("\n[LANGUAGE SELECTOR / SELECTOR DE IDIOMA]")
    print(" [1] Español (es)")
    print(" [2] English (en)")

    while True:
        lang_choice = input("Select language / Seleccione idioma [1-2]: ").strip()
        if lang_choice == "1":
            lang = "es"
            break
        elif lang_choice == "2":
            lang = "en"
            break
        print("[ERROR] Invalid choice / Opción inválida.")

    while True:
        print("\n" + TEXTS[lang]["title"])
        print(TEXTS[lang]["opt1"])
        print(TEXTS[lang]["opt2"])
        print(TEXTS[lang]["opt3"])
        print(TEXTS[lang]["opt4"])
        print(TEXTS[lang]["opt5"])
        print(TEXTS[lang]["opt6"])
        print(TEXTS[lang]["opt0"])

        opcion = input(TEXTS[lang]["select_opt"]).strip()

        if opcion == "1":
            print(f"\n-> {TEXTS[lang]['opt1']}")
            entrada_usuario = input(TEXTS[lang]["ask_city"]).strip()

            if entrada_usuario:

                resolution = resolve_zumper_city(entrada_usuario)
                base_url = build_zumper_url(resolution)

                print("[INFO] Ciudad detectada:", resolution.city)
                print("[INFO] Fuente:", resolution.source)
                print(f"[INFO] URL Objetivo: {base_url}")

                html_crudo = fetch_html_content(base_url)

                if html_crudo:
                    propiedades_limpias = parse_listings_html(html_crudo)

                    if propiedades_limpias:
                        from database_mod.db_manager import save_properties_to_db

                        # 🔥 GUARDAMOS LA CIUDAD
                        last_city = resolution.city

                        # 🔥 PASAMOS LA CIUDAD
                        if save_properties_to_db(propiedades_limpias, last_city):
                            print(f"\n[SUCCESS] Datos guardados: {len(propiedades_limpias)} inmuebles registrados.")
                        else:
                            print("[ERROR] Falló la escritura en la base de datos.")
                    else:
                        print("[ALERT] No se extrajeron listados válidos.")

        elif opcion == "2":
            print(f"\n-> {TEXTS[lang]['opt2']}")

            # 🔥 VALIDACIÓN PRO
            if not last_city:
                print("[WARNING] Primero debes escanear una ciudad (opción 1).")
                continue

            if generate_market_report(city=last_city, lang=lang):
                print("[SUCCESS] Reporte Excel generado.")

                if generate_market_chart(last_city, lang):
                    print("[SUCCESS] Gráfico corporativo exportado.")

                # 🔥 NUEVO: LISTINGS CHART
                if generate_listings_chart(last_city, lang):
                    print("[SUCCESS] Gráfico de listings exportado.")

        elif opcion == "3":
            print(f"\n-> {TEXTS[lang]['opt3']}")
            clear_generated_reports()

        elif opcion == "4":
            print(f"\n-> {TEXTS[lang]['opt4']}")
            clear_database()
            clear_generated_reports()

            last_city = None

            print("[WARNING] Sistema restablecido a estado de fábrica.")



        elif opcion == "5":

            print(f"\n-> {TEXTS[lang]['opt5']}")

            cities = get_cities_from_db()

            if not cities:
                print("[WARNING] No hay ciudades disponibles en la base de datos.")

                continue

            print("\n📍 Ciudades disponibles:\n")

            for i, city in enumerate(cities, 1):
                print(f"[{i}] {city}")

            try:

                choice = int(input("\nSelecciona la ciudad: ").strip())

                if choice < 1 or choice > len(cities):
                    print("[ERROR] Selección inválida.")

                    continue

                selected_city = cities[choice - 1]

                print(f"\n[INFO] Enviando reporte de: {selected_city}")

                if send_market_report_email(lang, selected_city):
                    print("[SUCCESS] Reporte enviado correctamente.")


            except ValueError:

                print("[ERROR] Debes ingresar un número válido.")



        elif opcion == "6":

            print("\n[INFO] Enviando TODOS los reportes disponibles...")

            if send_full_report_email(lang):

                print("[SUCCESS] Reporte completo enviado correctamente.")

            else:

                print("[ERROR] No se pudo enviar el reporte completo.")

        elif opcion == "0":
            print("\n" + TEXTS[lang]["goodbye"])
            sys.exit(0)