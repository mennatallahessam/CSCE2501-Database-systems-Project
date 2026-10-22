# -*- coding: utf-8 -*-
"""
crawler/parse.py
-----------------
Pure-function HTML parser: raw bytes → structured dict.

All functions are side-effect free so they are unit-testable with saved samples.
Returns None for any field that cannot be confidently extracted (never guesses).

Field mapping  (site → schema):
  ld+json Product.brand.name          → developer_name
  ld+json Product.additionalProperty  → area_name, property_type, delivery_status, delivery_year
  ld+json Product.offers.price        → asking_price
  ld+json Product.description         → description
  <h1>                                → project_name (development)
  page text "النوع"                   → property_type (fallback)
  page text "المساحة"                 → total_area_sqm
  page text "غرف"                     → num_bedrooms
  page text "حمامات"                  → num_bathrooms
  page text "التشطيب"                 → finishing
  page text "سنة التعاقد"             → contract_year
  page text "سعر المتر بالتعاقد"      → price_per_sqm (at contract)
  page text "مكسبك عن سعر السوق"      → gain_over_market (EGP)
  page text "سعر السوق اليوم"         → market_price
  page text "المطلوب كاش دلوقتي"      → asking_price (fallback)
  dl "المتبقي للمطور"                 → remaining_to_developer
  dl "القسط"                          → installment_amount, installment_frequency
  dl "باقي على خلاص التقسيط"         → remaining_installment_years
  dl "الاستلام"                       → delivery_year (fallback)
  <span> "U-XXXXX"                   → listing_code
  ✓ / amenity text around checkmarks → amenities list
  URL slug                            → source_url, property_uuid
"""

import json
import logging
import re
from typing import Any

from bs4 import BeautifulSoup, Tag

log = logging.getLogger(__name__)

# ── Arabic-Indic digit normalizer ────────────────────────────────────────────
_ARABIC_INDIC = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def _normalise_digits(text: str) -> str:
    """Convert Arabic-Indic digits to ASCII digits."""
    return text.translate(_ARABIC_INDIC)


# ── Number extraction helpers ─────────────────────────────────────────────────

def _parse_num(text: str | None) -> float | None:
    """
    Extract the first numeric value from an Arabic/English mixed string.
    Handles commas (thousands separators), Arabic-Indic digits, and
    'مليون' (million) suffix.
    Returns None on failure — never guesses.
    """
    if not text:
        return None
    text = _normalise_digits(text)
    # Handle "X.Y مليون" or "X مليون"
    million = re.search(r"([\d,.]+)\s*مليون", text)
    if million:
        try:
            return float(million.group(1).replace(",", "")) * 1_000_000
        except ValueError:
            pass
    # Plain number (with optional commas and decimal)
    m = re.search(r"([\d,]+(?:\.\d+)?)", text)
    if m:
        try:
            return float(m.group(1).replace(",", ""))
        except ValueError:
            pass
    return None


def _parse_int(text: str | None) -> int | None:
    v = _parse_num(text)
    return int(v) if v is not None else None


# ── Property-type normalizer ──────────────────────────────────────────────────

# Map Arabic / English spelling variants → canonical schema values
_TYPE_MAP: dict[str, str] = {
    # Arabic
    "شقة": "apartment",
    "شقه": "apartment",
    "فيلا": "villa",
    "فيلانا": "villa",
    "تاون هاوس": "townhouse",
    "تاون هاووس": "townhouse",
    "تاونهاوس": "townhouse",
    "توين هاوس": "townhouse",
    "توين هاووس": "townhouse",
    "دوبلكس": "duplex",
    "دوبليكس": "duplex",
    "بنتهاوس": "penthouse",
    "بنت هاوس": "penthouse",
    "شاليه": "chalet",
    "شاليهة": "chalet",
    "ستوديو": "studio",
    "استوديو": "studio",
    # English
    "apartment": "apartment",
    "villa": "villa",
    "townhouse": "townhouse",
    "twin house": "townhouse",
    "twin villa": "villa",
    "duplex": "duplex",
    "penthouse": "penthouse",
    "chalet": "chalet",
    "studio": "studio",
}


def _normalise_type(raw: str | None) -> str | None:
    if not raw:
        return None
    key = raw.strip().lower()
    result = _TYPE_MAP.get(key)
    if result is None:
        log.debug("Unmapped property type: %r", raw)
    return result or "other"


# ── Payment method normalizer ─────────────────────────────────────────────────

def _detect_payment_method(soup: BeautifulSoup) -> str:
    """Return 'cash' or 'installment' based on page signals."""
    text = soup.get_text()
    if "كاش" in text or "cash" in text.lower():
        # Also check for installment signals
        if any(kw in text for kw in ["قسط", "تقسيط", "أقساط"]):
            return "installment"
        return "cash"
    if any(kw in text for kw in ["قسط", "تقسيط", "أقساط"]):
        return "installment"
    return "cash"


# ── ld+json extraction ────────────────────────────────────────────────────────

def _extract_ldjson(soup: BeautifulSoup) -> dict[str, Any]:
    """Extract the Schema.org Product block from ld+json scripts."""
    result: dict[str, Any] = {}
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except (json.JSONDecodeError, TypeError):
            continue

        if data.get("@type") == "Product":
            result["name"] = data.get("name", "")
            result["description"] = data.get("description", "")
            result["url"] = data.get("url", "")
            # Brand → developer name
            brand = data.get("brand", {})
            if isinstance(brand, dict):
                result["developer_name"] = brand.get("name", "")
            # Offers → asking price
            offers = data.get("offers", {})
            if isinstance(offers, dict):
                result["asking_price"] = offers.get("price")
                result["currency"] = offers.get("priceCurrency", "EGP")
            # additionalProperty
            props = data.get("additionalProperty", [])
            for prop in props:
                pname = prop.get("name", "")
                pval = prop.get("value")
                if pname in ("المنطقة", "المنطقة الجغرافية"):
                    result["area_name"] = pval
                elif pname == "نوع الوحدة":
                    result["unit_type_raw"] = pval
                elif pname in ("حالة الاستلام", "الحالة"):
                    result["delivery_status"] = pval
                elif pname in ("سنة الاستلام", "الاستلام"):
                    result["delivery_year_ld"] = _parse_int(str(pval))
            break  # Only need the first Product block

    return result


# ── dl/dt/dd financial block ─────────────────────────────────────────────────

def _extract_dl_fields(soup: BeautifulSoup) -> dict[str, Any]:
    """Parse definition list entries for financial / installment data."""
    result: dict[str, Any] = {}
    for dl in soup.find_all("dl"):
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        for dt_el, dd_el in zip(dts, dds):
            label = dt_el.get_text(strip=True)
            value = dd_el.get_text(strip=True)

            if "المتبقي للمطور" in label or "متبقي للمطور" in label:
                result["remaining_to_developer"] = _parse_num(value)
            elif "القسط" == label.strip():
                # "594,227 ج.م · ربع سنوي"
                result["installment_amount"] = _parse_num(value)
                # Frequency
                if "شهري" in value:
                    result["installment_frequency"] = "monthly"
                elif "ربع سنوي" in value or "ربعي" in value:
                    result["installment_frequency"] = "quarterly"
                elif "نصف سنوي" in value or "نصف‌سنوي" in value:
                    result["installment_frequency"] = "semi-annual"
                elif "سنوي" in value:
                    result["installment_frequency"] = "annual"
            elif "باقي على خلاص التقسيط" in label or "باقي التقسيط" in label:
                result["remaining_installment_years"] = _parse_num(value)
            elif "الاستلام" == label.strip():
                result["delivery_year_dl"] = _parse_int(value)

    return result


# ── Main page-text field extraction ──────────────────────────────────────────

def _find_value_after_label(text: str, label: str) -> str | None:
    """
    In the page's concatenated text, find the value that appears right after
    an Arabic label.  Returns the next non-empty token.
    """
    idx = text.find(label)
    if idx == -1:
        return None
    # Take the substring after the label and grab first meaningful token
    after = text[idx + len(label):].lstrip("\n\r :")
    # First line or up to 80 chars
    line = after.split("\n")[0].strip()[:80]
    return line if line else None


def _extract_page_text_fields(soup: BeautifulSoup) -> dict[str, Any]:
    """Extract structured fields from the raw page text using label search."""
    text = soup.get_text(separator="\n", strip=True)
    text = _normalise_digits(text)

    result: dict[str, Any] = {}

    # Property type (النوع)
    val = _find_value_after_label(text, "النوع")
    if val:
        result["property_type_raw"] = val.strip()

    # Area
    val = _find_value_after_label(text, "المساحة")
    if val:
        result["total_area_sqm"] = _parse_num(val)

    # Bedrooms (label is standalone "غرف" after a number)
    m = re.search(r"(\d+)\s*\n?غرف", text)
    if m:
        result["num_bedrooms"] = int(m.group(1))

    # Bathrooms
    m = re.search(r"(\d+)\s*\n?حمامات", text)
    if m:
        result["num_bathrooms"] = int(m.group(1))

    # Finishing
    val = _find_value_after_label(text, "التشطيب")
    if val:
        result["finishing"] = val.strip()

    # Contract year
    val = _find_value_after_label(text, "سنة التعاقد")
    if val:
        result["contract_year"] = _parse_int(val)

    # Garden/roof area
    val = _find_value_after_label(text, "جاردن/رووف")
    if val:
        result["garden_roof_sqm"] = _parse_num(val)

    # Price per sqm at contract
    val = _find_value_after_label(text, "سعر المتر بالتعاقد")
    if val:
        result["price_per_sqm_contract"] = _parse_num(val)

    # Asking price (cash label)
    m = re.search(r"المطلوب كاش دلوقتي\s*\n?([\d,،.]+)\s*ج\.م", text)
    if m:
        result["asking_price_text"] = _parse_num(m.group(1))

    # Gain over market value
    m = re.search(r"مكسبك عن سعر السوق.*?\n\+?\s*([\d,،.]+)\s*ج\.م", text)
    if m:
        result["gain_over_market_egp"] = _parse_num(m.group(1))

    # Market price today
    m = re.search(r"سعر السوق اليوم\s*[:\n].*?([\d,،.]+)\s*ج\.م", text)
    if m:
        result["market_price"] = _parse_num(m.group(1))

    return result


# ── Amenity extraction ────────────────────────────────────────────────────────

# Known amenity keywords (Arabic and English)
_AMENITY_KEYWORDS = [
    "مصعد", "حمام سباحة", "بيسين", "جيم", "نادي رياضي", "جراج", "موقف",
    "حديقة", "جاردن", "أمن", "حراسة", "سكيوريتي", "كلوب هاوس", "مول",
    "بحيرة", "لاجون", "بحر", "شاطئ", "تراس", "رووف", "بلكونة",
    "تكييف مركزي", "فيو بحر", "فيو جولف",
    "swimming pool", "gym", "garage", "parking", "garden", "security",
    "elevator", "club house", "lake", "sea view", "golf view",
]


def _extract_amenities(soup: BeautifulSoup) -> list[str]:
    """
    Extract amenities from:
    1. Checkmark (✓) items on the page
    2. Description text (keyword match)
    """
    amenities: list[str] = []

    # 1. Checkmark items: look for ✓ symbol followed by text
    page_text = soup.get_text(separator="\n")
    lines = page_text.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("✓") or line == "✓":
            # The amenity name is either in this line or the next
            amenity = line.lstrip("✓").strip()
            if not amenity and i + 1 < len(lines):
                amenity = lines[i + 1].strip()
            if amenity and len(amenity) < 60:
                amenities.append(amenity)

    # 2. Keyword match in description
    desc = soup.get_text().lower()
    for kw in _AMENITY_KEYWORDS:
        if kw.lower() in desc and kw not in amenities:
            amenities.append(kw)

    # Deduplicate preserving order
    seen: set[str] = set()
    unique = []
    for a in amenities:
        if a not in seen:
            seen.add(a)
            unique.append(a)
    return unique


# ── Listing code extraction ───────────────────────────────────────────────────

def _extract_listing_code(soup: BeautifulSoup) -> str | None:
    """Extract the site's internal listing code like 'U-19440'."""
    m = re.search(r"\bU-\d+\b", soup.get_text())
    return m.group(0) if m else None


# ── Location extraction ───────────────────────────────────────────────────────

def _extract_location(soup: BeautifulSoup, ld_area: str | None) -> dict[str, str | None]:
    """
    Build a location dict from breadcrumb / page text / ld+json area_name.
    Returns keys: city, district, area_name, compound_name
    """
    location: dict[str, str | None] = {
        "city": None,
        "district": None,
        "area_name": ld_area,
        "compound_name": None,
    }

    # Try to extract from the subtitle paragraph  "<developer> · <location> · <type>"
    h1 = soup.find("h1")
    if h1:
        sibling_p = h1.find_next_sibling("p")
        if sibling_p:
            parts = [p.strip() for p in sibling_p.get_text().split("·") if p.strip()]
            # parts[0] = developer, parts[1] = location, parts[2] = type
            if len(parts) >= 2:
                location["area_name"] = parts[1]

    return location


# ── Master parse function ─────────────────────────────────────────────────────

def parse_property_page(html: bytes, source_url: str) -> dict[str, Any] | None:
    """
    Parse a raw HTML property page into a structured dict.

    Returns None if the page is clearly not a valid property page
    (e.g. redirect to home, error page, Cloudflare challenge).

    All monetary values are in EGP.
    """
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception as exc:
        log.error("BS4 parse error for %s: %s", source_url, exc)
        return None

    # Sanity check — reject non-property pages
    title = soup.title.string if soup.title else ""
    if not title or "just a moment" in title.lower():
        log.warning("Non-property page at %s (title=%r)", source_url, title)
        return None

    # Extract UUID from URL
    uuid_match = re.search(
        r"/buy/opportunity/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        source_url,
        re.IGNORECASE,
    )
    property_uuid = uuid_match.group(1) if uuid_match else None

    # ── Gather all field groups ───────────────────────────────────────────────
    ld = _extract_ldjson(soup)
    dl_fields = _extract_dl_fields(soup)
    text_fields = _extract_page_text_fields(soup)
    amenities = _extract_amenities(soup)
    listing_code = _extract_listing_code(soup)
    location = _extract_location(soup, ld.get("area_name"))

    # ── Resolve property_type ──────────────────────────────────────────────────
    raw_type = ld.get("unit_type_raw") or text_fields.get("property_type_raw")
    property_type = _normalise_type(raw_type)

    # ── Resolve asking_price ──────────────────────────────────────────────────
    asking_price = (
        ld.get("asking_price")
        or text_fields.get("asking_price_text")
    )

    # ── Resolve delivery year ─────────────────────────────────────────────────
    delivery_year = ld.get("delivery_year_ld") or dl_fields.get("delivery_year_dl")

    # ── Compute derived metrics ───────────────────────────────────────────────
    area = text_fields.get("total_area_sqm")
    price_per_sqm: float | None = None
    if asking_price and area and area > 0:
        price_per_sqm = round(asking_price / area, 2)

    gain_egp = text_fields.get("gain_over_market_egp")
    market_price = text_fields.get("market_price")
    gain_pct: float | None = None
    if gain_egp and asking_price and asking_price > 0:
        gain_pct = round(gain_egp / asking_price * 100, 2)

    # ── Project name (h1) ─────────────────────────────────────────────────────
    h1 = soup.find("h1")
    project_name = h1.get_text(strip=True) if h1 else None

    # ── Build result ──────────────────────────────────────────────────────────
    result: dict[str, Any] = {
        # Identity
        "source_url": source_url,
        "property_uuid": property_uuid,
        "listing_code": listing_code,
        # Property
        "title": title.split(" | ")[0].strip() if title else None,
        "description": ld.get("description") or None,
        "property_type": property_type,
        "property_type_raw": raw_type,
        "total_area_sqm": area,
        "num_bedrooms": text_fields.get("num_bedrooms"),
        "num_bathrooms": text_fields.get("num_bathrooms"),
        "finishing": text_fields.get("finishing"),
        "garden_roof_sqm": text_fields.get("garden_roof_sqm"),
        # Financial
        "asking_price": asking_price,
        "price_per_sqm": price_per_sqm,
        "price_per_sqm_contract": text_fields.get("price_per_sqm_contract"),
        "market_price": market_price,
        "gain_over_market_egp": gain_egp,
        "gain_over_market_pct": gain_pct,
        "payment_method": _detect_payment_method(soup),
        "contract_year": text_fields.get("contract_year"),
        "delivery_year": delivery_year,
        "delivery_status": ld.get("delivery_status"),
        # Installments
        "remaining_to_developer": dl_fields.get("remaining_to_developer"),
        "installment_amount": dl_fields.get("installment_amount"),
        "installment_frequency": dl_fields.get("installment_frequency"),
        "remaining_installment_years": dl_fields.get("remaining_installment_years"),
        # Development / developer
        "project_name": project_name,
        "developer_name": ld.get("developer_name"),
        # Location
        "city": location.get("city"),
        "district": location.get("district"),
        "area_name": location.get("area_name"),
        "compound_name": location.get("compound_name"),
        # Amenities
        "amenities": amenities,
    }

    return result
