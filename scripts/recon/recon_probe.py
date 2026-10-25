"""Phase 0 Reconnaissance Script — AqarExit.
Fetches the listing page and a couple of property detail pages.
Saves raw responses to ./samples/ for offline analysis.
Prints a field inventory and data source summary.
"""
import json
import os
import re
import time
import urllib.robotparser
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36 "
        "(student project, CSCE 2501 AUC)"
    ),
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

BASE_URL = "https://aqarexit.com"
LISTING_URL = "https://aqarexit.com/en/opportunities?show=8000"
SAMPLES_DIR = Path(__file__).resolve().parent.parent.parent / "samples"
SAMPLES_DIR.mkdir(exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)


def fetch(url: str, label: str) -> requests.Response | None:
    print(f"\n[FETCH] {label}: {url}")
    try:
        r = session.get(url, timeout=20, allow_redirects=True)
        print(f"  Status: {r.status_code}  Content-Type: {r.headers.get('Content-Type','')}")
        print(f"  Final URL: {r.url}")
        print(f"  Bytes received: {len(r.content)}")
        return r
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def save(name: str, content: bytes | str, ext: str = "html"):
    path = SAMPLES_DIR / f"{name}.{ext}"
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    print(f"  Saved → {path}")


def check_robots():
    print("\n=== robots.txt ===")
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{BASE_URL}/robots.txt")
    rp.read()
    for url in [LISTING_URL, f"{BASE_URL}/en/opportunities/1"]:
        allowed = rp.can_fetch("*", url)
        print(f"  can_fetch(*, {url}) = {allowed}")
    # Also print the raw robots.txt
    r = session.get(f"{BASE_URL}/robots.txt", timeout=10)
    print(f"\n--- robots.txt content ---\n{r.text[:2000]}\n")
    save("robots", r.text, "txt")


def probe_listing_page():
    print("\n=== Listing Page Probe ===")
    r = fetch(LISTING_URL, "listing page")
    if not r:
        return None, None
    save("listing_page", r.content)

    soup = BeautifulSoup(r.content, "lxml")

    # 1. Check for embedded JSON (__NEXT_DATA__, __INITIAL_STATE__, ld+json)
    print("\n--- Checking for embedded JSON ---")
    next_data = soup.find("script", {"id": "__NEXT_DATA__"})
    if next_data:
        print("  ✓ Found <script id='__NEXT_DATA__'>")
        try:
            data = json.loads(next_data.string)
            save("next_data", json.dumps(data, ensure_ascii=False, indent=2), "json")
            return r, data
        except Exception as e:
            print(f"  Parse error: {e}")

    # Check for window.__INITIAL_STATE__
    for script in soup.find_all("script"):
        text = script.string or ""
        if "__INITIAL_STATE__" in text or "window.__" in text:
            print(f"  ✓ Found window.__ variable in script tag")
            save("initial_state_script", text, "js")

    # Check for ld+json
    ld_scripts = soup.find_all("script", {"type": "application/ld+json"})
    print(f"  ld+json blocks found: {len(ld_scripts)}")
    for i, s in enumerate(ld_scripts[:3]):
        print(f"    [{i}] {(s.string or '')[:200]}")

    return r, None


def probe_html_structure(soup: BeautifulSoup):
    """Inspect the HTML structure to find property cards."""
    print("\n--- HTML Structure ---")
    # Look for common property card patterns
    for selector in ["[class*='property']", "[class*='card']", "[class*='listing']",
                      "[class*='opportunity']", "[class*='unit']", "article", ".item"]:
        elements = soup.select(selector)
        if elements:
            print(f"  selector '{selector}': {len(elements)} elements found")
            if len(elements) > 0:
                print(f"    sample classes: {elements[0].get('class')}")

    # Links that look like property detail pages
    links = soup.find_all("a", href=re.compile(r'/en/(opportunities|properties|units)/\d+'))
    print(f"\n  Property-like links found: {len(links)}")
    unique_urls = list(set(a.get("href", "") for a in links))[:10]
    for u in unique_urls:
        print(f"    {u}")
    return unique_urls


def probe_detail_page(path: str, label: str):
    url = f"{BASE_URL}{path}" if path.startswith("/") else path
    r = fetch(url, label)
    if not r:
        return
    save(label, r.content)
    soup = BeautifulSoup(r.content, "lxml")
    print(f"\n--- Fields found on {label} ---")
    # Try to extract common fields
    for selector, field in [
        ("[class*='price']", "price"),
        ("[class*='area']", "area"),
        ("[class*='bedroom']", "bedrooms"),
        ("[class*='bathroom']", "bathrooms"),
        ("[class*='title']", "title"),
        ("[class*='description']", "description"),
        ("[class*='type']", "type"),
        ("[class*='location']", "location"),
    ]:
        els = soup.select(selector)[:2]
        for el in els:
            txt = el.get_text(strip=True)[:120]
            if txt:
                print(f"  [{field}] {txt}")


def main():
    check_robots()

    listing_r, next_data = probe_listing_page()
    if not listing_r:
        print("FATAL: Could not fetch listing page.")
        return

    soup = BeautifulSoup(listing_r.content, "lxml")

    # Check if Cloudflare challenge page
    page_title = soup.title.string if soup.title else ""
    print(f"\nPage title: {page_title}")
    if "just a moment" in page_title.lower() or "cloudflare" in page_title.lower():
        print("⚠️  CLOUDFLARE CHALLENGE DETECTED — need headless browser or different approach")
        return

    # Probe HTML structure and get some property URLs
    property_urls = probe_html_structure(soup)

    # Try to find any API endpoints in script tags
    print("\n--- API endpoint hints in scripts ---")
    for script in soup.find_all("script"):
        text = script.string or ""
        for pattern in [r'https?://[^\s"\']+api[^\s"\']+', r'/api/[^\s"\']+']:
            matches = re.findall(pattern, text)
            for m in matches[:5]:
                print(f"  API hint: {m}")

    # Count total properties from listing
    all_links = soup.find_all("a", href=True)
    property_hrefs = [a["href"] for a in all_links if re.search(r'/(opportunities|properties)/\d+', a["href"])]
    unique_props = list(set(property_hrefs))
    print(f"\nTotal unique property links on listing page: {len(unique_props)}")
    if unique_props:
        save("property_urls", "\n".join(unique_props), "txt")

    # Probe a couple of detail pages
    time.sleep(2)
    if property_urls:
        probe_detail_page(property_urls[0], "detail_page_1")
        time.sleep(2)
        if len(property_urls) > 1:
            probe_detail_page(property_urls[1], "detail_page_2")

    print("\n=== RECON COMPLETE — check ./samples/ for raw files ===")


if __name__ == "__main__":
    main()
