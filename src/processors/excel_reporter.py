import pandas as pd
import os
from database_mod.db_manager import get_connection
from config.settings import REPORTS_DIR


# ==============================
# 🌍 DICCIONARIO BILINGÜE
# ==============================
HEADERS = {
    "es": {
        "summary_sheet": "Resumen del Mercado",
        "history_sheet": "Historial de Precios",
        "title": "Título del Inmueble",
        "rooms": "Habitaciones",
        "baths": "Baños",
        "price": "Precio Actual",
        "last_update": "Última Actualización",
        "link": "Enlace Web",
        "scan_date": "Fecha de Escaneo",
        "recorded_price": "Precio Registrado"
    },
    "en": {
        "summary_sheet": "Market Summary",
        "history_sheet": "Price History",
        "title": "Property Title",
        "rooms": "Rooms",
        "baths": "Bathrooms",
        "price": "Current Price",
        "last_update": "Last Update",
        "link": "Web Link",
        "scan_date": "Scan Date",
        "recorded_price": "Recorded Price"
    }
}


def generate_market_report(lang="es", city=None):

    labels = HEADERS.get(lang, HEADERS["es"])

    from config.settings import get_excel_filename

    file_name = get_excel_filename(city)
    excel_path = REPORTS_DIR / file_name

    # 🧹 borrar archivo anterior
    if excel_path.exists():
        try:
            os.remove(excel_path)
        except Exception as e:
            print(f"[WARNING] No se pudo borrar el reporte anterior: {e}")

    conn = get_connection()

    if city:
        query_history = """
            SELECT p.title, p.property_url, p.rooms, p.baths, h.price, h.capture_date
            FROM price_history h
            JOIN properties p ON h.property_id = p.id
            WHERE LOWER(p.city) = LOWER(?)
            ORDER BY h.capture_date DESC
        """
        df_history = pd.read_sql_query(query_history, conn, params=(city,))
    else:
        query_history = """
            SELECT p.title, p.property_url, p.rooms, p.baths, h.price, h.capture_date
            FROM price_history h
            JOIN properties p ON h.property_id = p.id
            ORDER BY h.capture_date DESC
        """
        df_history = pd.read_sql_query(query_history, conn)

    if df_history.empty:
        print("[ERROR] No se encontraron datos en la base de datos para generar el reporte.")
        conn.close()
        return False

    # ==============================
    # 📊 SUMMARY (CON baths)
    # ==============================
    df_summary = df_history.sort_values("capture_date") \
        .groupby("property_url").last().reset_index()

    df_summary = df_summary[[
        "title", "rooms", "baths", "price", "capture_date", "property_url"
    ]]

    df_summary.columns = [
        labels["title"],
        labels["rooms"],
        labels["baths"],
        labels["price"],
        labels["last_update"],
        labels["link"]
    ]

    # ==============================
    # 📊 HISTORY (SIN baths)
    # ==============================
    df_history_output = df_history[[
        "capture_date",
        "title",
        "rooms",
        "price",
        "property_url"
    ]].copy()

    df_history_output.columns = [
        labels["scan_date"],
        labels["title"],
        labels["rooms"],
        labels["recorded_price"],
        labels["link"]
    ]

    # ==============================
    # 📁 EXPORT EXCEL
    # ==============================
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:

        df_summary.to_excel(writer, sheet_name=labels["summary_sheet"], index=False)
        df_history_output.to_excel(writer, sheet_name=labels["history_sheet"], index=False)

        workbook = writer.book

        header_format = workbook.add_format({
            "bold": True,
            "text_wrap": True,
            "font_color": "#FFFFFF",
            "bg_color": "#1F4E78",
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        })

        data_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter",
            "text_wrap": True
        })

        money_format = workbook.add_format({
            "num_format": "$#,##0.00",
            "align": "center",
            "valign": "vcenter"
        })

        # ==============================
        # FORMATO HOJAS
        # ==============================
        for sheet_name in [labels["summary_sheet"], labels["history_sheet"]]:

            worksheet = writer.sheets[sheet_name]
            df_to_use = df_summary if sheet_name == labels["summary_sheet"] else df_history_output

            # headers
            for col_num, value in enumerate(df_to_use.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # altura de filas para que el wrap se vea bien
            for row in range(1, len(df_to_use) + 1):
                worksheet.set_row(row, 30)

            # =========================
            # 📊 FORMATO EXCEL FINAL
            # =========================

            num_cols = len(df_to_use.columns)

            # 1. Centrado general (TODAS las columnas)
            worksheet.set_column(0, num_cols - 1, None, data_format)

            # 2. Auto ancho + mantener centrado (SIN romper formato)
            for i, col in enumerate(df_to_use.columns):
                max_len = max(df_to_use[col].astype(str).map(len).max(), len(col)) + 3
                col_width = min(max_len, 50)

                if i == 0:
                    worksheet.set_column(i, i, 45, data_format)  # títulos más visibles
                else:
                    worksheet.set_column(i, i, min(col_width, 30), data_format)  # compacto pro

            # 3. Formato especial para PRICE (sobrescribe lo anterior)
            price_col_idx = 3  # (ajusta si cambias estructura del DF)

            worksheet.set_column(
                price_col_idx,
                price_col_idx,
                18,
                money_format
            )

            conn.close()

    print(f"[SUCCESS] Reporte de mercado generado exitosamente en: {excel_path}")
    return True