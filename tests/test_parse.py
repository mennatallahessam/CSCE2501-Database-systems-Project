# -*- coding: utf-8 -*-
"""
tests/test_parse.py
--------------------
Unit tests for crawler/parse.py using saved sample pages.

Run with:
    pytest tests/test_parse.py -v

Tests cover:
- parse_property_page returns a dict (not None) for each sample
- key fields are extracted and non-empty
- Arabic text (description) is decoded correctly
- Numeric fields are floats/ints, not strings
- Property type normalised to schema vocabulary
- Price per sqm derived correctly
- Amenities list is non-empty where expected
- Arabic-Indic digits handled
"""

import sys
from pathlib import Path

import pytest

# Allow running tests from any directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crawler.parse import (
    _normalise_digits,
    _normalise_type,
    _parse_num,
    parse_property_page,
)
from etl.clean import clean

# ── Helpers ────────────────────────────────────────────────────────────────────

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"
SAMPLE_FILES = sorted(SAMPLES_DIR.glob("detail_*.html"))

# Skip whole module if no samples saved yet
pytestmark = pytest.mark.skipif(
    not SAMPLE_FILES,
    reason="No sample HTML files in ./samples/ — run recon_detail.py first",
)


# ── Unit tests: helper functions ───────────────────────────────────────────────

class TestNormaliseDigits:
    def test_arabic_indic(self):
        assert _normalise_digits("١٢٣٤٥") == "12345"

    def test_mixed(self):
        assert _normalise_digits("3 غرف") == "3 غرف"

    def test_pure_ascii(self):
        assert _normalise_digits("12345") == "12345"


class TestParseNum:
    def test_simple(self):
        assert _parse_num("8,500,000") == 8_500_000.0

    def test_million_arabic(self):
        result = _parse_num("8.5 مليون")
        assert result == pytest.approx(8_500_000.0)

    def test_with_currency(self):
        assert _parse_num("8,500,000 ج.م") == 8_500_000.0

    def test_arabic_indic_digits(self):
        assert _parse_num("١٥٥") == 155.0

    def test_none_on_empty(self):
        assert _parse_num("") is None
        assert _parse_num(None) is None

    def test_none_on_text_only(self):
        assert _parse_num("لا يوجد") is None


class TestNormaliseType:
    def test_arabic_apartment(self):
        assert _normalise_type("شقة") == "apartment"

    def test_arabic_penthouse(self):
        assert _normalise_type("بنتهاوس") == "penthouse"

    def test_arabic_duplex(self):
        assert _normalise_type("دوبلكس") == "duplex"

    def test_arabic_chalet(self):
        assert _normalise_type("شاليه") == "chalet"

    def test_english_villa(self):
        assert _normalise_type("villa") == "villa"

    def test_unknown_maps_to_other(self):
        assert _normalise_type("وحدة مجهولة") == "other"

    def test_none(self):
        assert _normalise_type(None) is None


# ── Integration tests: parse sample HTML files ────────────────────────────────

@pytest.fixture(params=SAMPLE_FILES, ids=[p.name for p in SAMPLE_FILES])
def sample_result(request):
    html_path: Path = request.param
    html = html_path.read_bytes()
    url = f"https://aqarexit.com/buy/opportunity/{html_path.stem.split('_')[-1]}"
    result = parse_property_page(html, url)
    return result


class TestParsePropertyPage:
    def test_returns_dict(self, sample_result):
        assert sample_result is not None
        assert isinstance(sample_result, dict)

    def test_has_source_url(self, sample_result):
        assert "source_url" in sample_result
        assert sample_result["source_url"].startswith("https://")

    def test_has_title(self, sample_result):
        assert sample_result.get("title")

    def test_property_type_valid(self, sample_result):
        valid = {"apartment", "villa", "townhouse", "duplex",
                 "chalet", "penthouse", "studio", "other", None}
        assert sample_result.get("property_type") in valid

    def test_asking_price_numeric(self, sample_result):
        price = sample_result.get("asking_price")
        if price is not None:
            assert isinstance(price, (int, float))
            assert price > 0

    def test_area_numeric(self, sample_result):
        area = sample_result.get("total_area_sqm")
        if area is not None:
            assert isinstance(area, (int, float))
            assert area > 0

    def test_amenities_list(self, sample_result):
        amenities = sample_result.get("amenities")
        assert isinstance(amenities, list)

    def test_description_is_string_or_none(self, sample_result):
        desc = sample_result.get("description")
        assert desc is None or isinstance(desc, str)

    def test_arabic_description_decoded(self, sample_result):
        """Description should contain Arabic characters (not garbled bytes)."""
        desc = sample_result.get("description")
        if desc:
            # At least some characters should be in Arabic Unicode range
            arabic_chars = [c for c in desc if "\u0600" <= c <= "\u06ff"]
            assert len(arabic_chars) > 0, f"No Arabic chars in description: {desc!r}"

    def test_project_name_present(self, sample_result):
        # Project name comes from h1 — should be present in valid pages
        assert sample_result.get("project_name") is not None

    def test_bedrooms_sane(self, sample_result):
        beds = sample_result.get("num_bedrooms")
        if beds is not None:
            assert 0 <= beds <= 20

    def test_bathrooms_sane(self, sample_result):
        baths = sample_result.get("num_bathrooms")
        if baths is not None:
            assert 0 <= baths <= 20


# ── Clean pipeline integration ────────────────────────────────────────────────

class TestCleanPipeline:
    """Run the clean() step on top of parse() for each sample."""

    def test_clean_does_not_crash(self, sample_result):
        cleaned = clean(sample_result)
        assert isinstance(cleaned, dict)

    def test_price_per_sqm_derived(self, sample_result):
        cleaned = clean(sample_result)
        price = cleaned.get("asking_price")
        area = cleaned.get("total_area_sqm")
        ppsm = cleaned.get("price_per_sqm")
        if price and area and area > 0:
            expected = round(price / area, 2)
            assert ppsm == pytest.approx(expected, rel=1e-3)

    def test_property_type_in_schema_vocab(self, sample_result):
        cleaned = clean(sample_result)
        valid = {"apartment", "villa", "townhouse", "duplex",
                 "chalet", "penthouse", "studio", "other"}
        assert cleaned.get("property_type") in valid

    def test_payment_method_valid(self, sample_result):
        cleaned = clean(sample_result)
        assert cleaned.get("payment_method") in ("cash", "installment")
