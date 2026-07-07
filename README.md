# 🏠 Real Estate Scraper Pro

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

[🇺🇸 English](#-english-version) | [🇪🇸 Español](#-versión-en-español)
---

# 🇺🇸 English Version

## 🚀 Overview

**Real Estate Scraper Pro** is a professional Python system for **real estate data scraping, analysis, reporting, and visualization**.

It automates data extraction, stores it in a structured database, generates reports, and provides a web dashboard for interaction.

---

## 💼 Business Value

This project simulates a **real-world real estate data pipeline**, similar to systems used by:

- Property analytics companies  
- Real estate investors  
- Market research teams  

It demonstrates the ability to:

- Automate data extraction at scale  
- Build structured data pipelines  
- Generate business-ready reports  
- Deliver insights through dashboards  

👉 This is not just a scraper — it's a **complete data solution**.

## ✨ Features

- 🔎 Web scraping (Zumper)
- 🗄️ SQLite database
- 📊 Excel reports with historical tracking
- 📈 Chart generation (PNG)
- 📧 Email automation (TLS)
- 🧹 Data cleanup tools
- 🌐 Flask dashboard
- 🧩 Modular architecture

---

## 🏗️ System Architecture

| Component | Responsibility |
|----------|----------------|
| `main.py` | Data processing, scraping, reports, cleanup |
| `app.py` | Visualization and report interaction |

---

## 🔄 Workflow (Real Usage)

### Step 1 — Run Core System

```bash
python main.py
```

- Select language (EN/ES)
- Choose option **[1] Scan Data**
- Enter a city (miami, tampa, etc.)

👉 System will:
- Scrape data (Selenium)
- Parse HTML (BeautifulSoup)
- Store data in SQLite

---

### Step 2 — Generate Reports

```
[2] Generate Reports
```
👉 System generates:

- Excel file
- Market chart (PNG)
- Listings chart (PNG)

---

### Step 3 — Send Reports (Optional)

- `[5]` → Send report for ONE city  
- `[6]` → Send ALL reports  

---

## 🧠 CLI Menu

```
[1] Scan Data → Scrape and store listings  
[2] Generate Reports → Excel + charts  
[3] Clean Files → Delete generated files  
[4] Clear Database → Delete all data  
[5] Send Email → One city  
[6] Send All → All reports  
[0] Exit  
```

⚠️ Important:

* Run **[1] before [2]**
* If reports don’t exist → email will fail

---

## 📸 Screenshots

### 📊 Charts

**Detailed Listings Chart**
![chart\_detailed](screenshots/chart_detailed.png)

**Grouped Beds Chart**
![chart\_grouped](screenshots/chart_grouped.png)

---

### 🖥️ Console Execution

**Scraping Process**
![console\_process](screenshots/console_process.png)

**Successful Results**
![console\_success](screenshots/console_success.png)

---

### 📄 Excel Report
![excel_report](screenshots/excel_report.png)

---

### 🌐 Web Dashboard

![web\_dashboard](screenshots/web_dashboard.png)

---

## 📄 Excel Reports

### `Daily Results`

* Current scraping data
* Detailed information

### `Historical Data`

* Full history
* Tracks price changes

⚠️ Logic:

* No UPDATE
* Only INSERT
---

## 📄 Environment Configuration

This project uses environment variables for sensitive data.

### `.env.example`

```env
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_RECEIVER=
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

⚠️ Important:
- Never upload your real `.env` file
- Always use `.env.example` as reference

---

## ⚙️ Installation

```bash
git clone https://github.com/victor-veira-py/real-estate-scraper-pro.git
cd real-estate-scraper-pro
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 🌐 Run Dashboard

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000/
```

---

## 🚀 Future Improvements

- Docker containerization  
- Automated scheduled scraping (cron jobs)  
- Multi-city batch processing optimization  
- Advanced dashboard filters and analytics  
- Authentication system for dashboard  

---

## 🛠️ Technologies

- Python  
- Selenium  
- BeautifulSoup  
- SQLite  
- Pandas  
- Matplotlib  
- Flask  
- python-dotenv  

---

## 👨‍💻 Author

Víctor Armando De Oliveira Rodríguez  

---

## 📌 License

MIT License  

---

# 🇪🇸 Versión en Español

## 🚀 Descripción

**Real Estate Scraper Pro** es un sistema profesional en Python para scraping, análisis, reportes y visualización de datos inmobiliarios.

---

## 💼 Valor del Proyecto

Este proyecto simula un **pipeline de datos inmobiliarios del mundo real**, demostrando:

- Automatización de scraping  
- Procesamiento y almacenamiento estructurado  
- Generación de reportes listos para negocio  
- Visualización mediante dashboard  

👉 No es solo un scraper, es una **solución completa de datos**.
---

## ✨ Funcionalidades

- 🔎 Scraping desde Zumper
- 🗄️ Base de datos SQLite
- 📊 Excel con historial
- 📈 Gráficos PNG
- 📧 Envío de correos (TLS)
- 🧹 Limpieza de datos
- 🌐 Dashboard Flask

---

## 🏗️ Arquitectura

| Componente | Función |
|----------|--------|
| `main.py` | Scraping, procesamiento, reportes |
| `app.py` | Visualización |

---

## 🔄 Flujo REAL

### Paso 1 - Ejecutar sistema

```bash
python main.py
```

* Elegir idioma
* Opción **[1] Escanear**
* Ingresar ciudad

---

### Paso 2

```
[2] Generar Reportes
```

Genera:

* Excel
* Gráficos

---

### Paso 3 — Enviar (Opcional)

* `[5]` → Una ciudad
* `[6]` → Todas

---

## 🧠 Menú

```
[1] Escanear
[2] Reportes
[3] Limpiar archivos
[4] Vaciar DB
[5] Enviar uno
[6] Enviar todo
[0] Salir
```

⚠️ Importante:

* Ejecutar [1] antes de [2]

---

## 📸 Capturas

### 📊 Gráficos

**Gráfico de Listados Detallados**
![chart\_detailed](screenshots/chart_detailed.png)

****Gráfica por Número de Habitaciones/Camas****
![chart\_grouped](screenshots/chart_grouped.png)

---

### 🖥️ Consola

**Proceso de Scraping**
![console\_process](screenshots/console_process.png)

**Resultados Exitosos**
![console\_success](screenshots/console_success.png)

---

### 📄 Reporte en Excel
![excel\_report](screenshots/excel_report.png)

---

### 🌐 Dashboard Web

![web\_dashboard](screenshots/web_dashboard.png)

---

## 📄 Excel

- Daily Results → datos actuales  
- Historical Data → historial completo  

⚠️ Solo INSERT (sin UPDATE)

--- 

## 📄 Configuración de Entorno

Este proyecto utiliza variables de entorno para manejar información sensible.

### `.env.example`

```env
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_RECEIVER=
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

⚠️ Importante:
- Nunca subas tu archivo real `.env`
- Usa siempre `.env.example` como referencia
- El archivo `.env` contiene credenciales sensibles y debe mantenerse privado

--- 

## ⚙️ Instalación

```bash
git clone https://github.com/victor-veira-py/real-estate-scraper-pro.git
cd real-estate-scraper-pro
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 🚀 Futuras Mejoras

- Docker  
- Automatización con cron  
- Multi-ciudad optimizado  
- Filtros avanzados en dashboard  
- Sistema de autenticación  

---

## 💯 Autor

Víctor Armando De Oliveira Rodríguez  

---

## 📌 Licencia

MIT License  