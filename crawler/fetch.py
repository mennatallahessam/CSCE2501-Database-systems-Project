# -*- coding: utf-8 -*-
"""
crawler/fetch.py
-----------------
Polite, resumable, idempotent HTTP fetcher.

State is persisted in a SQLite database (crawl_state.sqlite).
Raw HTML responses are cached to ./raw/<slug>.html so parsing can be
re-run without re-crawling.

Usage (from project root):
    python -m crawler.fetch [--urls PATH] [--limit N]

Options:
    --urls  Path to URL list file (default: ./samples/property_urls.txt)
    --limit N  Stop after N downloads (useful for testing)
"""

import argparse
import hashlib
import logging
import random
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    BACKOFF_BASE,
    CIRCUIT_BREAK_THRESHOLD,
    DELAY_MAX,
    DELAY_MIN,
    MAX_RETRIES,
    RAW_DIR,
    REQUEST_TIMEOUT,
    STATE_DB,
    USER_AGENT,
)

log = logging.getLogger(__name__)

# ── SQLite state helpers ─────────────────────────────────────────────────────


def _slug(url: str) -> str:
    """Derive a safe filesystem name from a URL (last path component)."""
    return url.rstrip("/").split("/")[-1]


def init_state_db(db_path: str = STATE_DB) -> sqlite3.Connection:
    """Create (or open) the crawl-state SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crawl_state (
            url          TEXT PRIMARY KEY,
            property_id  TEXT,
            status       TEXT NOT NULL DEFAULT 'pending',
            http_status  INTEGER,
            attempts     INTEGER NOT NULL DEFAULT 0,
            fetched_at   TEXT
        )
    """)
    conn.commit()
    return conn


def seed_urls(conn: sqlite3.Connection, urls: list[str]) -> None:
    """Insert URLs that aren't already tracked (idempotent)."""
    conn.executemany(
        "INSERT OR IGNORE INTO crawl_state (url, property_id, status) VALUES (?, ?, 'pending')",
        [(url, _slug(url)) for url in urls],
    )
    conn.commit()


def pending_urls(conn: sqlite3.Connection) -> list[str]:
    """Return URLs that still need to be fetched."""
    rows = conn.execute(
        "SELECT url FROM crawl_state WHERE status IN ('pending', 'failed') AND attempts < ?",
        (MAX_RETRIES,),
    ).fetchall()
    return [r["url"] for r in rows]


def mark_done(conn: sqlite3.Connection, url: str, http_status: int) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """UPDATE crawl_state
           SET status='done', http_status=?, attempts=attempts+1, fetched_at=?
           WHERE url=?""",
        (http_status, now, url),
    )
    conn.commit()


def mark_failed(conn: sqlite3.Connection, url: str, http_status: int | None) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """UPDATE crawl_state
           SET status='failed', http_status=?, attempts=attempts+1, fetched_at=?
           WHERE url=?""",
        (http_status, now, url),
    )
    conn.commit()


# ── HTTP session ─────────────────────────────────────────────────────────────


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept-Language": "ar,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
        }
    )
    return session


# ── Fetch with retry and exponential backoff ─────────────────────────────────


def fetch_url(
    session: requests.Session,
    url: str,
    attempt: int = 1,
) -> tuple[int | None, bytes | None]:
    """
    Fetch a single URL.

    Returns (http_status, body_bytes).
    Returns (None, None) on connection-level failure.
    """
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        return r.status_code, r.content
    except requests.exceptions.Timeout:
        log.warning("Timeout on %s (attempt %d)", url, attempt)
        return None, None
    except requests.exceptions.ConnectionError as exc:
        log.warning("Connection error on %s: %s (attempt %d)", url, exc, attempt)
        return None, None
    except Exception as exc:
        log.error("Unexpected error fetching %s: %s", url, exc)
        return None, None


def crawl(
    urls: list[str],
    conn: sqlite3.Connection,
    limit: int | None = None,
    raw_dir: Path = Path(RAW_DIR),
) -> None:
    """
    Main crawl loop — polite, resumable, cached.

    Respects circuit-breaker: stops after CIRCUIT_BREAK_THRESHOLD consecutive errors.
    """
    raw_dir.mkdir(parents=True, exist_ok=True)
    session = build_session()

    total = len(urls)
    done_count = 0
    fail_count = 0
    consecutive_errors = 0
    start_time = time.time()

    for i, url in enumerate(urls):
        if limit and done_count >= limit:
            log.info("Reached limit of %d. Stopping.", limit)
            break

        slug = _slug(url)
        cache_path = raw_dir / f"{slug}.html"

        # Skip if already cached on disk and marked done
        if cache_path.exists():
            log.debug("Cache hit for %s — skipping fetch.", slug)
            mark_done(conn, url, 200)
            done_count += 1
            continue

        # Polite delay
        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        time.sleep(delay)

        # Retry loop
        status, body = None, None
        for attempt in range(1, MAX_RETRIES + 1):
            status, body = fetch_url(session, url, attempt)

            if status is None:
                # Connection-level failure — backoff and retry
                wait = BACKOFF_BASE ** attempt
                log.warning("Attempt %d/%d failed for %s. Backoff %.1fs.", attempt, MAX_RETRIES, url, wait)
                if attempt < MAX_RETRIES:
                    time.sleep(wait)
                continue

            if status == 200:
                break

            if status in (429, 503):
                # Rate-limited — honour Retry-After header if present
                log.warning("Rate limited (%d) on %s attempt %d.", status, url, attempt)
                wait = BACKOFF_BASE ** attempt
                log.info("Backing off %.1fs before retry.", wait)
                time.sleep(wait)
                continue

            if status in (403, 503) and body and b"cloudflare" in (body or b"").lower():
                log.error("Cloudflare challenge on %s. Stopping crawl.", url)
                mark_failed(conn, url, status)
                return  # hard stop

            if status >= 400:
                log.warning("HTTP %d on %s. Not retrying.", status, url)
                break

        # Evaluate outcome
        if status == 200 and body:
            cache_path.write_bytes(body)
            mark_done(conn, url, 200)
            done_count += 1
            consecutive_errors = 0
        else:
            mark_failed(conn, url, status)
            fail_count += 1
            consecutive_errors += 1
            log.warning("Failed %s (status=%s, consecutive=%d)", url, status, consecutive_errors)

        # Circuit breaker
        if consecutive_errors >= CIRCUIT_BREAK_THRESHOLD:
            log.error(
                "Circuit breaker triggered: %d consecutive errors. Stopping cleanly.",
                consecutive_errors,
            )
            break

        # Progress log every 50 items
        if (i + 1) % 50 == 0:
            elapsed = time.time() - start_time
            rate = (done_count + fail_count) / elapsed if elapsed > 0 else 0
            remaining = total - (done_count + fail_count)
            eta_min = (remaining / rate / 60) if rate > 0 else float("inf")
            log.info(
                "Progress: %d/%d done=%d failed=%d rate=%.2f/s ETA=%.0fmin",
                i + 1, total, done_count, fail_count, rate, eta_min,
            )

    log.info("Crawl finished. done=%d failed=%d total=%d", done_count, fail_count, total)


# ── CLI ───────────────────────────────────────────────────────────────────────


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("crawl.log", encoding="utf-8"),
        ],
    )

    parser = argparse.ArgumentParser(description="Fetch AqarExit property pages.")
    parser.add_argument(
        "--urls",
        default="./samples/property_urls.txt",
        help="Path to URL list (one per line).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Stop after N successful downloads.",
    )
    args = parser.parse_args()

    url_file = Path(args.urls)
    if not url_file.exists():
        print(f"URL file not found: {url_file}. Run crawler/discover.py first.")
        sys.exit(1)

    urls = [u.strip() for u in url_file.read_text("utf-8").splitlines() if u.strip()]
    print(f"Loaded {len(urls)} URLs from {url_file}")

    conn = init_state_db()
    seed_urls(conn, urls)

    pending = pending_urls(conn)
    print(f"Pending (not yet fetched): {len(pending)}")

    if not pending:
        print("Nothing to do — all URLs already done.")
        return

    crawl(pending, conn, limit=args.limit)


if __name__ == "__main__":
    main()
