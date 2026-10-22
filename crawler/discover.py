# -*- coding: utf-8 -*-
"""
crawler/discover.py
-------------------
Enumerate all property URLs from the AqarExit sitemap.

Usage:
    python -m crawler.discover [--out PATH]

Output: a plain text file with one URL per line (sitemap order).
The sitemap URL pattern is: https://aqarexit.com/buy/opportunity/<uuid>
which is the robots-allowed path.
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import requests

# Allow running as a script from the project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import SITEMAP_URL, USER_AGENT, REQUEST_TIMEOUT

log = logging.getLogger(__name__)

PROPERTY_URL_RE = re.compile(
    r"<loc>(https://aqarexit\.com(?:/en)?/buy/opportunity/[0-9a-f\-]+)</loc>",
    re.IGNORECASE,
)


def fetch_sitemap(sitemap_url: str = SITEMAP_URL) -> str:
    """Download the sitemap and return its text content."""
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    log.info("Fetching sitemap: %s", sitemap_url)
    r = session.get(sitemap_url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    log.info("Sitemap size: %d bytes", len(r.content))
    return r.text


def extract_property_urls(sitemap_text: str) -> list[str]:
    """Return deduplicated list of property detail-page URLs found in the sitemap."""
    urls = PROPERTY_URL_RE.findall(sitemap_text)
    # Normalise to the English (non-/en/) path so we always hit one canonical URL
    normalised: list[str] = []
    seen: set[str] = set()
    for url in urls:
        # Strip /en/ prefix if present so we use the base URL
        canonical = url.replace("/en/buy/", "/buy/")
        if canonical not in seen:
            seen.add(canonical)
            normalised.append(canonical)
    log.info("Found %d unique property URLs in sitemap.", len(normalised))
    return normalised


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    parser = argparse.ArgumentParser(description="Discover all AqarExit property URLs.")
    parser.add_argument(
        "--out",
        default="./samples/property_urls.txt",
        help="Output file path (one URL per line).",
    )
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sitemap_text = fetch_sitemap()
    urls = extract_property_urls(sitemap_text)

    out_path.write_text("\n".join(urls), encoding="utf-8")
    print(f"Discovered {len(urls)} property URLs → {out_path}")


if __name__ == "__main__":
    main()
