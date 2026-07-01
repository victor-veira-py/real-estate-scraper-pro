import re
from dataclasses import dataclass
from typing import Optional, Dict
from geopy.geocoders import Nominatim


# ==============================
# 1. BASE DE DATOS PRINCIPAL
# ==============================

ZUMPER_CITY_MAP: Dict[str, str] = {
    "new york": "new-york-ny",
    "los angeles": "los-angeles-ca",
    "chicago": "chicago-il",
    "houston": "houston-tx",
    "phoenix": "phoenix-az",
    "philadelphia": "philadelphia-pa",
    "san antonio": "san-antonio-tx",
    "san diego": "san-diego-ca",
    "dallas": "dallas-tx",
    "san jose": "san-jose-ca",
    "austin": "austin-tx",
    "jacksonville": "jacksonville-fl",
    "fort worth": "fort-worth-tx",
    "columbus": "columbus-oh",
    "charlotte": "charlotte-nc",
    "san francisco": "san-francisco-ca",
    "indianapolis": "indianapolis-in",
    "seattle": "seattle-wa",
    "denver": "denver-co",
    "washington": "washington-dc",
    "boston": "boston-ma",
    "el paso": "el-paso-tx",
    "detroit": "detroit-mi",
    "nashville": "nashville-tn",
    "portland": "portland-or",
    "las vegas": "las-vegas-nv",
    "oklahoma city": "oklahoma-city-ok",
    "louisville": "louisville-ky",
    "baltimore": "baltimore-md",
    "milwaukee": "milwaukee-wi",
    "albuquerque": "albuquerque-nm",
    "tucson": "tucson-az",
    "fresno": "fresno-ca",
    "sacramento": "sacramento-ca",
    "mesa": "mesa-az",
    "kansas city": "kansas-city-mo",
    "atlanta": "atlanta-ga",
    "miami": "miami-fl",
    "orlando": "orlando-fl",
    "tampa": "tampa-fl",
    "cleveland": "cleveland-oh",
    "pittsburgh": "pittsburgh-pa",
    "cincinnati": "cincinnati-oh",
    "raleigh": "raleigh-nc",
    "minneapolis": "minneapolis-mn",
    "st louis": "st-louis-mo",
    "new orleans": "new-orleans-la",
    "honolulu": "honolulu-hi",
    "anchorage": "anchorage-ak"
}


# ==============================
# 2. GEOCODER (fallback externo)
# ==============================

geolocator = Nominatim(user_agent="uacs_city_resolver")


# ==============================
# 3. UTILIDADES
# ==============================

def normalize_city(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def slug(text: str) -> str:
    return text.lower().strip().replace(" ", "-")


# ==============================
# 4. RESOLVER PRINCIPAL
# ==============================

@dataclass
class CityResolution:
    city: str
    state: Optional[str]
    slug: str
    source: str  # "map" | "geopy" | "fallback"


def resolve_zumper_city(user_input: str) -> CityResolution:
    city_raw = normalize_city(user_input)

    # ==========================
    # CAPA 1: MAPA FIJO (FASTEST)
    # ==========================
    if city_raw in ZUMPER_CITY_MAP:
        return CityResolution(
            city=city_raw,
            state=None,
            slug=ZUMPER_CITY_MAP[city_raw],
            source="map"
        )

    # ==========================
    # CAPA 2: GEOPY STRUCTURED
    # ==========================
    try:
        location = geolocator.geocode(f"{city_raw}, USA", addressdetails=True)

        if location:
            addr = location.raw.get("address", {})

            city = (
                addr.get("city")
                or addr.get("town")
                or addr.get("village")
                or city_raw
            )

            state = addr.get("state")

            # intenta mapear estado a slug si existe
            state_code = STATE_MAP.get(state.lower()) if state else None

            if state_code:
                return CityResolution(
                    city=city,
                    state=state_code,
                    slug=f"{slug(city)}-{state_code}",
                    source="geopy"
                )

            return CityResolution(
                city=city,
                state=None,
                slug=slug(city),
                source="geopy"
            )

    except Exception as e:
        print(f"[GEOPY ERROR] {e}")

    # ==========================
    # CAPA 3: FALLBACK FINAL
    # ==========================
    return CityResolution(
        city=city_raw,
        state=None,
        slug=slug(city_raw),
        source="fallback"
    )


# ==============================
# 5. STATE MAP (para geopy)
# ==============================

STATE_MAP = {
    "florida": "fl",
    "california": "ca",
    "new york": "ny",
    "texas": "tx",
    "nevada": "nv",
    "illinois": "il",
    "georgia": "ga",
    "arizona": "az",
    "colorado": "co",
    "washington": "wa",
    "oregon": "or",
    "massachusetts": "ma",
    "pennsylvania": "pa",
    "ohio": "oh",
    "michigan": "mi",
    "minnesota": "mn",
    "missouri": "mo",
    "north carolina": "nc",
    "south carolina": "sc",
    "tennessee": "tn",
    "louisiana": "la",
    "virginia": "va",
    "new jersey": "nj",
    "maryland": "md",
    "wisconsin": "wi",
    "kentucky": "ky",
    "indiana": "in",
    "oklahoma": "ok",
    "utah": "ut",
    "kansas": "ks",
    "iowa": "ia",
    "nebraska": "ne",
    "new mexico": "nm",
    "alabama": "al",
    "mississippi": "ms",
    "arkansas": "ar",
    "idaho": "id",
    "montana": "mt",
    "wyoming": "wy",
    "north dakota": "nd",
    "south dakota": "sd",
    "alaska": "ak",
    "hawaii": "hi"
}


# ==============================
# 6. URL BUILDER FINAL
# ==============================

def build_zumper_url(city_resolution: CityResolution) -> str:
    return f"https://www.zumper.com/apartments-for-rent/{city_resolution.slug}"