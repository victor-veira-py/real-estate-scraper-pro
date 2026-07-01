import sqlite3
from datetime import datetime
from config.settings import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ AÑADIMOS city
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_url TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            rooms TEXT,
            baths TEXT,
            city TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            price REAL NOT NULL,
            capture_date TEXT NOT NULL,
            FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def save_properties_to_db(lista_propiedades, city):
    """
    Ahora recibe city 🔥
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for prop in lista_propiedades:

            # ✅ INSERT CON CITY
            cursor.execute("""
                INSERT OR IGNORE INTO properties (property_url, title, rooms, baths, city)
                VALUES (?, ?, ?, ?, ?)
            """, (
                prop['property_url'],
                prop['title'],
                prop.get('rooms', 'N/A'),
                prop.get('baths', 'N/A'),
                city
            ))

            cursor.execute("SELECT id FROM properties WHERE property_url = ?", (prop['property_url'],))
            prop_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO price_history (property_id, price, capture_date)
                VALUES (?, ?, ?)
            """, (prop_id, prop['price'], fecha_actual))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"[DB ERROR] Error al guardar en base de datos: {e}")
        return False


def clear_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM price_history")
        cursor.execute("DELETE FROM properties")

        conn.commit()
        conn.close()
        print("[SUCCESS] Base de datos SQLite completamente vaciada.")
        return True

    except Exception as e:
        print(f"[DB ERROR] Fallo al limpiar la base de datos: {e}")
        return False