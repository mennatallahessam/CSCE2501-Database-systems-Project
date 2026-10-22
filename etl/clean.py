# -*- coding: utf-8 -*-
"""
etl/clean.py
-------------
Normalization and derived-field computation.

Input:  raw parsed dict from crawler/parse.py
Output: cleaned dict ready for database insertion

Canonical type vocabulary (matches schema CHECK constraint):
    'apartment' | 'villa' | 'townhouse' | 'duplex' |
    'chalet' | 'penthouse' | 'studio' | 'other'

Derived metrics (documented here for README):
    price_per_sqm = asking_price / total_area_sqm          (if both > 0)
    gain_over_market (pct) = gain_over_market_egp / asking_price * 100
    discount_over_market = market_price - asking_price      (if both present)
"""

import logging
import re
from typing import Any

log = logging.getLogger(__name__)

# ── Location normalisation ────────────────────────────────────────────────────

# Map common variant spellings → canonical city/area names
_LOCATION_NORM: dict[str, str] = {
    "الساحل الشمالي": "الساحل الشمالي",
    "north coast": "الساحل الشمالي",
    "التجمع الخامس": "التجمع الخامس",
    "new cairo": "التجمع الخامس",
    "6 أكتوبر": "6 أكتوبر",
    "6 اكتوبر": "6 أكتوبر",
    "october": "6 أكتوبر",
    "القاهرة الجديدة": "القاهرة الجديدة",
    "مدينة نصر": "مدينة نصر",
    "الشيخ زايد": "الشيخ زايد",
    "sheikh zayed": "الشيخ زايد",
    "الرحاب": "الرحاب",
    "العاصمة الإدارية": "العاصمة الإدارية",
    "العاصمة الادارية": "العاصمة الإدارية",
    "new capital": "العاصمة الإدارية",
    "مدينتي": "مدينتي",
    "الضبعة": "الضبعة",
    "الغردقة": "الغردقة",
    "hurghada": "الغردقة",
    "العين السخنة": "العين السخنة",
    "ain sokhna": "العين السخنة",
    "الإسماعيلية": "الإسماعيلية",
    "زهراء المعادي": "زهراء المعادي",
    "المعادي": "المعادي",
    "مصر الجديدة": "مصر الجديدة",
}


def _normalise_text(text: str | None) -> str | None:
    """Strip extra whitespace and normalise to consistent casing."""
    if not text:
        return None
    return " ".join(text.split())


def normalise_location(raw: str | None) -> str | None:
    """Normalise location string to canonical form."""
    if not raw:
        return None
    cleaned = _normalise_text(raw)
    if cleaned is None:
        return None
    key = cleaned.lower().strip()
    return _LOCATION_NORM.get(key, cleaned)


# ── Developer name normalisation ──────────────────────────────────────────────

def normalise_developer(raw: str | None) -> str | None:
    """Normalise developer name: strip extra spaces, title-case."""
    if not raw:
        return None
    name = _normalise_text(raw)
    # Remove common suffixes that duplicate meaning
    for suffix in [" company", " co.", " llc", " s.a.e", " s.a.e."]:
        if name and name.lower().endswith(suffix):
            name = name[: -len(suffix)].strip()
    return name


# ── Project name normalisation ────────────────────────────────────────────────

def normalise_project(raw: str | None) -> str | None:
    """Normalise project/development name."""
    if not raw:
        return None
    return _normalise_text(raw)


# ── Amenity normalisation ─────────────────────────────────────────────────────

_AMENITY_MAP: dict[str, str] = {
    "مصعد": "Elevator",
    "elevator": "Elevator",
    "حمام سباحة": "Swimming Pool",
    "بيسين": "Swimming Pool",
    "swimming pool": "Swimming Pool",
    "pool": "Swimming Pool",
    "جيم": "Gym",
    "gym": "Gym",
    "نادي رياضي": "Gym",
    "جراج": "Parking",
    "موقف": "Parking",
    "garage": "Parking",
    "parking": "Parking",
    "حديقة": "Garden",
    "جاردن": "Garden",
    "garden": "Garden",
    "أمن": "Security",
    "حراسة": "Security",
    "سكيوريتي": "Security",
    "security": "Security",
    "كلوب هاوس": "Club House",
    "club house": "Club House",
    "لاجون": "Lagoon",
    "بحيرة": "Lagoon",
    "lake": "Lagoon",
    "lagoon": "Lagoon",
    "بحر": "Sea View",
    "شاطئ": "Beach",
    "beach": "Beach",
    "تراس": "Terrace",
    "رووف": "Roof",
    "roof": "Roof",
    "بلكونة": "Balcony",
    "balcony": "Balcony",
    "تكييف مركزي": "Central AC",
    "central ac": "Central AC",
    "فيو بحر": "Sea View",
    "sea view": "Sea View",
    "فيو جولف": "Golf View",
    "golf view": "Golf View",
}


def normalise_amenities(raw_list: list[str]) -> list[str]:
    """Map raw amenity strings to canonical English names; deduplicate."""
    result: list[str] = []
    seen: set[str] = set()
    for item in raw_list:
        key = item.strip().lower()
        canonical = _AMENITY_MAP.get(key, item.strip())
        if canonical not in seen:
            seen.add(canonical)
            result.append(canonical)
    return result


# ── Numeric guards ────────────────────────────────────────────────────────────

def _guard_positive(value: float | None, field: str) -> float | None:
    """Return None (not zero) for implausible values; log for audit."""
    if value is None:
        return None
    if value <= 0:
        log.warning("Implausible %s=%s — storing NULL.", field, value)
        return None
    return value


def _guard_price_per_sqm(ppsm: float | None) -> float | None:
    """Prices per sqm outside 1k–5M EGP are likely bad data."""
    if ppsm is None:
        return None
    if ppsm < 1_000 or ppsm > 5_000_000:
        log.warning("Suspicious price_per_sqm=%.2f — storing NULL.", ppsm)
        return None
    return ppsm


# ── Master clean function ─────────────────────────────────────────────────────

def clean(raw: dict[str, Any]) -> dict[str, Any]:
    """
    Normalise and validate a raw parsed property dict.

    Never drops rows — flags problems as NULL and logs them.
    Returns a cleaned dict with the same keys plus computed columns.
    """
    out: dict[str, Any] = dict(raw)  # shallow copy

    # ── Strings ──────────────────────────────────────────────────────────────
    out["title"] = _normalise_text(raw.get("title"))
    out["description"] = _normalise_text(raw.get("description"))
    out["finishing"] = _normalise_text(raw.get("finishing"))
    out["delivery_status"] = _normalise_text(raw.get("delivery_status"))
    out["project_name"] = normalise_project(raw.get("project_name"))
    out["developer_name"] = normalise_developer(raw.get("developer_name"))

    # ── Location ─────────────────────────────────────────────────────────────
    out["area_name"] = normalise_location(raw.get("area_name"))
    out["city"] = normalise_location(raw.get("city")) or out["area_name"]
    out["district"] = _normalise_text(raw.get("district"))
    out["compound_name"] = _normalise_text(raw.get("compound_name"))

    # ── Numerics ─────────────────────────────────────────────────────────────
    area = _guard_positive(raw.get("total_area_sqm"), "total_area_sqm")
    out["total_area_sqm"] = area

    # ── Payment method & Price resolution ──────────────────────────────────────
    pm = raw.get("payment_method", "cash")
    out["payment_method"] = pm if pm in ("cash", "installment") else "cash"

    remaining = _guard_positive(raw.get("remaining_to_developer"), "remaining_to_developer")
    out["remaining_to_developer"] = remaining

    cash_now = _guard_positive(raw.get("asking_price"), "asking_price")

    if out["payment_method"] == "installment" and remaining:
        # On AqarExit resale, cash_now is the down payment (cash required now),
        # and remaining is the installment obligation to the developer.
        # Total asking price to own the unit = down_payment + remaining.
        out["down_payment"] = cash_now
        out["asking_price"] = round((cash_now or 0.0) + remaining, 2)
    else:
        out["down_payment"] = cash_now
        out["asking_price"] = cash_now

    asking = out["asking_price"]

    market = _guard_positive(raw.get("market_price"), "market_price")
    out["market_price"] = market

    # Derived: price_per_sqm
    if asking and area and area > 0:
        ppsm = round(asking / area, 2)
        out["price_per_sqm"] = _guard_price_per_sqm(ppsm)
    else:
        out["price_per_sqm"] = None

    # Derived: gain_over_market (EGP absolute) and percentage
    gain_egp = raw.get("gain_over_market_egp")
    out["gain_over_market_egp"] = gain_egp
    if gain_egp and asking and asking > 0:
        out["gain_over_market"] = round(gain_egp / asking * 100, 2)  # percent stored in schema
    else:
        out["gain_over_market"] = None

    # Derived: discount_over_market = market_price - asking_price
    if market and asking:
        out["discount_over_market"] = round(((market - asking) / market) * 100, 2)
    else:
        out["discount_over_market"] = None
    out["installment_amount"] = _guard_positive(
        raw.get("installment_amount"), "installment_amount"
    )
    out["remaining_installment_years"] = raw.get("remaining_installment_years")
    out["price_per_sqm_contract"] = _guard_price_per_sqm(
        raw.get("price_per_sqm_contract")
    )

    # Bedroom / bathroom sanity
    beds = raw.get("num_bedrooms")
    baths = raw.get("num_bathrooms")
    out["num_bedrooms"] = beds if (beds is not None and 0 <= beds <= 20) else None
    out["num_bathrooms"] = baths if (baths is not None and 0 <= baths <= 20) else None

    # Years
    cy = raw.get("contract_year")
    out["contract_year"] = cy if (cy and 1980 <= cy <= 2030) else None
    dy = raw.get("delivery_year")
    out["delivery_year"] = dy if (dy and 2000 <= dy <= 2040) else None

    # ── Amenities ─────────────────────────────────────────────────────────────
    out["amenities"] = normalise_amenities(raw.get("amenities") or [])

    # ── Payment method ────────────────────────────────────────────────────────
    pm = raw.get("payment_method", "cash")
    out["payment_method"] = pm if pm in ("cash", "installment") else "cash"

    # ── Property type ─────────────────────────────────────────────────────────
    pt = raw.get("property_type")
    valid_types = {"apartment", "villa", "townhouse", "duplex", "chalet", "penthouse", "studio", "other"}
    out["property_type"] = pt if pt in valid_types else "other"

    return out
