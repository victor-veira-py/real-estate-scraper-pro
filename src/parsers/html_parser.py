import re
from bs4 import BeautifulSoup


def parse_listings_html(html_content):
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    cards = soup.select("[data-testid='listing-card']")

    print(f"[PARSER] {len(cards)} cards detectadas")

    results = []
    seen_urls = set()

    for card in cards:
        try:
            # =========================
            # 🔗 LINK + TITLE
            # =========================
            a_tag = card.find("a", href=True)
            if not a_tag:
                continue

            href = a_tag["href"]

            if "/apartment-buildings/" not in href:
                continue

            full_url = "https://www.zumper.com" + href

            # evitar duplicados
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            title = a_tag.get_text(strip=True)

            # 🧹 VALIDACIÓN ROBUSTA
            if (
                    not title
                    or title.isdigit()
                    or len(title) < 4
                    or re.match(r"^\d+$", title)
            ):
                title = "Unknown Property"

            # =========================
            # 💰 PRICE (robusto + limpieza)
            # =========================
            raw_text = card.get_text().lower()

            # ❌ ignorar listings sin precio real
            if "contact" in raw_text or "call for" in raw_text:
                continue

            price = 0.0
            price_match = re.search(r"\$([\d,]+)", card.get_text())

            if price_match:
                price = float(price_match.group(1).replace(",", ""))

            # ❌ ignorar precios inválidos
            if price is None or price <= 0:
                continue

            # =========================
            # 🛏 ROOMS / BATHS
            # =========================
            rooms = "N/A"
            baths = "N/A"

            info_blocks = card.find_all("p")

            for block in info_blocks:
                txt = block.get_text(strip=True).lower()

                if "bed" in txt:
                    rooms = block.get_text(strip=True)

                if "bath" in txt:
                    baths = block.get_text(strip=True)

            # =========================
            # 📦 RESULTADO FINAL
            # =========================
            results.append({
                "property_url": full_url,
                "title": title,
                "rooms": rooms,
                "baths": baths,
                "price": price
            })

            print(f"[OK] {title[:30]} | ${price} | {rooms} | {baths}")

        except Exception as e:
            print(f"[ERROR CARD] {e}")

    return results