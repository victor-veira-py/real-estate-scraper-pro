import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import DB_PATH, ASSETS_DIR


TEXTS = {
    "es": {
        "title": "UACS - Precio Promedio en {city}",
        "xlabel": "Tipo de Propiedad (Rooms)",
        "ylabel": "Precio Promedio (USD)",
        "warning": "No hay datos para la ciudad",
        "success": "Gráfico generado correctamente en"
    },
    "en": {
        "title": "UACS - Average Price in {city}",
        "xlabel": "Property Type (Rooms)",
        "ylabel": "Average Price (USD)",
        "warning": "No data available for city",
        "success": "Chart successfully generated at"
    }
}


def normalize_rooms(value):
    if not value:
        return "Unknown"

    value = str(value).lower()

    if "studio" in value:
        return "Studio"
    if "1" in value and "2" in value:
        return "1-2 Beds"
    if "2" in value and "3" in value:
        return "2-3 Beds"

    return value


def generate_market_chart(city, language="es"):

    if not city or str(city).strip() == "":
        print("[ERROR] City inválida para generar gráfico")
        return False

    city = str(city).strip()

    if not DB_PATH.exists():
        print(f"[ERROR] No existe la base de datos en: {DB_PATH}")
        return False

    try:
        conn = sqlite3.connect(str(DB_PATH))

        query = """
            SELECT 
                p.rooms as habitacion,
                AVG(h.price) as precio_promedio
            FROM price_history h
            JOIN properties p ON p.id = h.property_id
            WHERE h.price IS NOT NULL 
              AND h.price > 0
              AND LOWER(p.city) = LOWER(?)
            GROUP BY p.rooms
        """

        df = pd.read_sql_query(query, conn, params=(city,))
        conn.close()

        txt = TEXTS.get(language, TEXTS["es"])

        if df.empty:
            print(f"[WARNING] {txt['warning']}: {city}")
            return False

        # =========================
        # 🔥 FIX REAL DEL PROBLEMA
        # =========================

        df["precio_promedio"] = pd.to_numeric(df["precio_promedio"], errors="coerce")
        df = df.dropna(subset=["precio_promedio"])

        # Normalizar habitaciones
        df["habitacion"] = df["habitacion"].apply(normalize_rooms)

        # 🔥 Agrupar correctamente
        df = df.groupby("habitacion", as_index=False)["precio_promedio"].mean()

        # 🔥 Forzar categorías fijas
        CATEGORIES = ["Studio", "1-2 Beds", "2-3 Beds", "3+ Beds", "Unknown"]
        df = df.set_index("habitacion").reindex(CATEGORIES).reset_index()

        # 🔥 Rellenar valores faltantes
        df["precio_promedio"] = df["precio_promedio"].fillna(0)


        # 🔥 Orden correcto
        df = df.sort_values(by="precio_promedio", ascending=False)

        # 🔥 Orden explícito
        order = df["habitacion"].tolist()

        sns.set_theme(style="whitegrid")

        fig, ax = plt.subplots(figsize=(12, 6))

        # 🔥 Palette inteligente (gris para valores en 0)
        palette = [
            "#cccccc" if v == 0 else c
            for v, c in zip(df["precio_promedio"], sns.color_palette("viridis", len(df)))
        ]

        sns.barplot(
            x="habitacion",
            y="precio_promedio",
            data=df,
            order=order,
            palette=palette
        )

        ax.set_title(txt["title"].format(city=city))
        ax.set_xlabel(txt["xlabel"])
        ax.set_ylabel(txt["ylabel"])

        plt.xticks(rotation=35, ha="right")

        # =========================
        # 🔥 FIX IMPORTANTE AQUÍ
        # =========================
        for p in ax.patches:
            height = p.get_height()
            ax.text(
                p.get_x() + p.get_width() / 2,
                height,
                f"${round(height, 2)}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()

        ASSETS_DIR.mkdir(parents=True, exist_ok=True)

        safe_city = city.lower().replace(" ", "_")
        save_path = ASSETS_DIR / f"grafico_{safe_city}.png"

        plt.savefig(save_path, dpi=160)
        plt.close(fig)

        print(f"[SUCCESS] {txt['success']}: {save_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Fallo al generar gráfico: {e}")
        return False


def generate_listings_chart(city, language="es", limit=10):
    """
    Muestra propiedades reales (NO promedio).
    Top N listings ordenados por precio.
    """

    if not city or str(city).strip() == "":
        print("[ERROR] City inválida")
        return False

    city = str(city).strip()

    if not DB_PATH.exists():
        print(f"[ERROR] No existe DB en: {DB_PATH}")
        return False

    try:
        conn = sqlite3.connect(str(DB_PATH))

        query = """
            SELECT 
                p.title as nombre,
                h.price as precio
            FROM price_history h
            JOIN properties p ON p.id = h.property_id
            WHERE h.price IS NOT NULL 
              AND h.price > 0
              AND LOWER(p.city) = LOWER(?)
        """

        df = pd.read_sql_query(query, conn, params=(city,))
        conn.close()

        txt = TEXTS.get(language, TEXTS["es"])

        if df.empty:
            print(f"[WARNING] {txt['warning']}: {city}")
            return False

        # 🔥 limpieza
        df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
        df = df.dropna(subset=["precio"])

        # 🔥 ordenar por precio real
        df = df.sort_values(by="precio", ascending=False).head(limit)

        # 🔥 colores
        palette = sns.color_palette("viridis", len(df))

        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12, 6))

        sns.barplot(
            x="nombre",
            y="precio",
            data=df,
            palette=palette
        )

        ax.set_title(f"{txt['title'].format(city=city)} (Listings)")
        ax.set_xlabel("Property Name")
        ax.set_ylabel("Price (USD)")

        plt.xticks(rotation=45, ha="right")

        # 🔥 etiquetas
        for p in ax.patches:
            height = p.get_height()
            ax.text(
                p.get_x() + p.get_width() / 2,
                height,
                f"${round(height, 2)}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()

        ASSETS_DIR.mkdir(parents=True, exist_ok=True)

        safe_city = city.lower().replace(" ", "_")
        save_path = ASSETS_DIR / f"listings_{safe_city}.png"

        plt.savefig(save_path, dpi=160)
        plt.close(fig)

        print(f"[SUCCESS] Listings chart generado en: {save_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Listings chart falló: {e}")
        return False