import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

from src.config.settings import (
    SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASS,
    EMAIL_RECEIVER, REPORTS_DIR, ASSETS_DIR
)
from src.config.settings import get_excel_filename


def send_market_report_email(lang="es", city=None):

    # =========================
    # 🔒 VALIDACIÓN
    # =========================
    if not all([SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):
        print("[ERROR] Configuración de correo incompleta en .env")
        return False

    if not city:
        print("[ERROR] No se recibió ciudad para generar el email")
        return False

    city = city.lower().replace(" ", "_")

    # =========================
    # 📎 ARCHIVOS DINÁMICOS
    # =========================
    excel_file = get_excel_filename(city)
    excel_path = REPORTS_DIR / excel_file

    market_png = ASSETS_DIR / f"grafico_{city}.png"
    listings_png = ASSETS_DIR / f"listings_{city}.png"

    print("[DEBUG] Excel:", excel_path)
    print("[DEBUG] Market PNG:", market_png)
    print("[DEBUG] Listings PNG:", listings_png)

    # =========================
    # 📨 EMAIL
    # =========================
    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER

    msg["Subject"] = (
        f"INFORME EJECUTIVO - {city.upper()}"
        if lang == "es"
        else f"EXECUTIVE REPORT - {city.upper()}"
    )

    # =========================
    # 🖼️ HTML BODY
    # =========================
    img_html = ""

    if market_png.exists():
        img_html += """
        <h3>Market Chart</h3>
        <div style="text-align:center;">
            <img src="cid:market_cid" style="max-width:100%; border:1px solid #ccc;">
        </div>
        """

    if listings_png.exists():
        img_html += """
        <h3>Listings Chart</h3>
        <div style="text-align:center;">
            <img src="cid:listings_cid" style="max-width:100%; border:1px solid #ccc;">
        </div>
        """

    html_body = f"""
    <html>
        <body style="font-family: Arial;">

            <h2>📊 Reporte Inmobiliario - {city.upper()}</h2>

            <p>{"Análisis completado automáticamente." if lang == "es"
            else "Automated analysis completed."}</p>

            {img_html}

            <p>{"Archivo Excel adjunto con el análisis completo." if lang == "es"
            else "Excel file attached with full analysis."}</p>

        </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    # =========================
    # 🖼️ IMAGEN MARKET INLINE
    # =========================
    if market_png.exists():
        with open(market_png, "rb") as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header("Content-ID", "<market_cid>")
            mime_img.add_header("Content-Disposition", "inline", filename="market.png")
            msg.attach(mime_img)

    # =========================
    # 🖼️ IMAGEN LISTINGS INLINE
    # =========================
    if listings_png.exists():
        with open(listings_png, "rb") as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header("Content-ID", "<listings_cid>")
            mime_img.add_header("Content-Disposition", "inline", filename="listings.png")
            msg.attach(mime_img)

    # =========================
    # 📎 EXCEL (SOLO CIUDAD ACTUAL)
    # =========================
    if excel_path.exists():
        with open(excel_path, "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)

            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={excel_file}"
            )

            msg.attach(attachment)
    else:
        print("[ERROR] Excel no encontrado:", excel_path)
        return False

    # =========================
    # 📤 SMTP
    # =========================
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

        print("[SUCCESS] Correo enviado correctamente")
        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    finally:
        try:
            server.quit()
        except:
            pass


def send_full_report_email(lang="es"):

    if not all([SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):
        print("[ERROR] Configuración de correo incompleta")
        return False

    # =========================
    # 🔥 AQUÍ ESTÁ EL FIX REAL
    # =========================
    excel_files = list(REPORTS_DIR.glob("reporte_*.xlsx"))

    png_files = list(ASSETS_DIR.glob("*.png"))

    if not png_files:
        print("[ERROR] No hay imágenes para enviar")
        return False

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "FULL MARKET REPORT (ALL CITIES)"

    body = f"""
    <h2>📊 Reporte completo</h2>
    <p>Se adjuntan todas las ciudades procesadas.</p>
    <p>Total imágenes: {len(png_files)}</p>
    """

    msg.attach(MIMEText(body, "html"))

    # =========================
    # 📎 EXCELS (TODAS LAS CIUDADES)
    # =========================
    for excel in excel_files:
        with open(excel, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={excel.name}"
            )
            msg.attach(part)

    # =========================
    # 📎 IMÁGENES (TODAS LAS CIUDADES)
    # =========================
    for png in png_files:
        with open(png, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={png.name}"
            )
            msg.attach(part)

    # =========================
    # 📤 SMTP
    # =========================
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        print("[SUCCESS] Email completo enviado")
        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    finally:
        try:
            server.quit()
        except:
            pass