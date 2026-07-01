from flask import Flask, render_template, request, redirect
import sys
from pathlib import Path

# 🔧 conectar con tu backend
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from database_mod.db_manager import get_connection
from tools.email_notifier import send_market_report_email, send_full_report_email
from processors.excel_reporter import generate_market_report
from visualizers.chart_generator import generate_market_chart, generate_listings_chart

app = Flask(__name__)

# 🔹 obtener ciudades
def get_cities():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT city FROM properties
        WHERE city IS NOT NULL
        ORDER BY city
    """)

    cities = [row[0] for row in cursor.fetchall()]
    conn.close()
    return cities


@app.route("/")
def index():
    cities = get_cities()
    return render_template("index.html", cities=cities)


@app.route("/generate", methods=["POST"])
def generate():
    city = request.form.get("city")

    generate_market_report(lang="en")
    generate_market_chart(city, "en")
    generate_listings_chart(city, "en")

    return redirect("/")


@app.route("/send", methods=["POST"])
def send():
    city = request.form.get("city")
    send_market_report_email("en", city)
    return redirect("/")


@app.route("/send_all", methods=["POST"])
def send_all():
    send_full_report_email("en")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)