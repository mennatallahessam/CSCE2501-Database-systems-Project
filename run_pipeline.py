# -*- coding: utf-8 -*-
"""
run_pipeline.py
----------------
Master end-to-end pipeline runner.

Stages:
  1. discover  - fetch sitemap, enumerate all property URLs
  2. fetch     - download all pages (polite, resumable)
  3. parse     - parse raw HTML → structured dicts
  4. clean     - normalise and derive computed fields
  5. load      - insert into MySQL (idempotent)
  6. seed      - generate synthetic users / reviews
  7. export    - dump all tables to CSV
  8. validate  - generate validation_report.md

Run the full pipeline:
    python run_pipeline.py

Run a small test (10 properties, skip fetch if raw/ already has files):
    python run_pipeline.py --limit 10

Skip to a specific stage:
    python run_pipeline.py --start-stage parse
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import os
import sys as _sys
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(_sys.stdout, "reconfigure"):
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("crawl.log", encoding="utf-8"),
    ],
)

STAGES = ["discover", "fetch", "parse", "clean", "load", "seed", "export", "validate"]


def stage_discover():
    """Fetch sitemap and write all property URLs to disk."""
    from crawler.discover import fetch_sitemap, extract_property_urls
    print("\n-- Stage 1: Discover ------------------------------")
    sitemap_text = fetch_sitemap()
    urls = extract_property_urls(sitemap_text)
    out = Path("./samples/property_urls.txt")
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(urls), encoding="utf-8")
    print(f"  {len(urls)} URLs → {out}")
    return urls


def stage_fetch(urls: list[str], limit: int | None = None):
    """Download all property HTML pages."""
    from crawler.fetch import init_state_db, seed_urls, pending_urls, crawl
    print("\n-- Stage 2: Fetch ---------------------------------")
    conn = init_state_db()
    seed_urls(conn, urls)
    pending = pending_urls(conn)
    print(f"  Pending: {len(pending)}")
    crawl(pending, conn, limit=limit)


def stage_parse_and_clean() -> list[dict]:
    """Parse all cached HTML files and clean the results."""
    from crawler.parse import parse_property_page
    from etl.clean import clean

    print("\n-- Stage 3+4: Parse & Clean -----------------------")
    raw_dir = Path("./raw")
    html_files = list(raw_dir.glob("*.html"))
    print(f"  Found {len(html_files)} cached HTML files.")

    records = []
    failed = 0
    for i, path in enumerate(html_files):
        slug = path.stem
        url = f"https://aqarexit.com/buy/opportunity/{slug}"
        try:
            raw_result = parse_property_page(path.read_bytes(), url)
            if raw_result is None:
                failed += 1
                continue
            cleaned = clean(raw_result)
            records.append(cleaned)
        except Exception as e:
            log.error("Parse/clean error for %s: %s", slug, e)
            failed += 1

        if (i + 1) % 500 == 0:
            print(f"  Parsed {i+1}/{len(html_files)}  ok={len(records)} failed={failed}")

    print(f"  Done: {len(records)} records, {failed} failures.")
    return records


def stage_load(records: list[dict]):
    """Load all cleaned records into MySQL."""
    from etl.load import load_all, get_connection, print_row_counts
    print("\n-- Stage 5: Load ----------------------------------")
    ok, fail = load_all(records)
    print(f"  Inserted: {ok}  Failed: {fail}")
    conn = get_connection()
    print_row_counts(conn)
    conn.close()


def stage_seed():
    """Seed synthetic users and reviews."""
    print("\n-- Stage 6: Seed Users & Reviews ------------------")
    from etl.seed_users import main as seed_main
    seed_main()


def stage_export():
    """Export all tables to CSV."""
    print("\n-- Stage 7: Export CSV ----------------------------")
    from etl.export_csv import main as export_main
    # Simulate CLI call
    import sys
    old_argv = sys.argv
    sys.argv = ["export_csv.py"]
    export_main()
    sys.argv = old_argv


def stage_validate():
    """Generate validation report."""
    print("\n-- Stage 8: Validate ------------------------------")
    from validation.validate import main as val_main
    val_main()


def main():
    parser = argparse.ArgumentParser(description="AqarExit end-to-end pipeline.")
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit fetching to N pages (for testing).",
    )
    parser.add_argument(
        "--start-stage", choices=STAGES, default="discover",
        help="Skip stages before this one (assumes earlier stages already ran).",
    )
    parser.add_argument(
        "--only-stage", choices=STAGES, default=None,
        help="Run only this single stage.",
    )
    args = parser.parse_args()

    start_idx = STAGES.index(args.start_stage)
    if args.only_stage:
        run_stages = [args.only_stage]
    else:
        run_stages = STAGES[start_idx:]

    print(f"Running stages: {run_stages}")
    if args.limit:
        print(f"Fetch limit: {args.limit} pages")

    urls: list[str] = []
    records: list[dict] = []

    if "discover" in run_stages:
        urls = stage_discover()

    if "fetch" in run_stages:
        if not urls:
            url_file = Path("./samples/property_urls.txt")
            if url_file.exists():
                urls = [u for u in url_file.read_text("utf-8").splitlines() if u.strip()]
        stage_fetch(urls, limit=args.limit)

    if "parse" in run_stages or "clean" in run_stages:
        records = stage_parse_and_clean()

    if "load" in run_stages:
        if not records:
            print("No records to load - run parse stage first.")
        else:
            stage_load(records)

    if "seed" in run_stages:
        stage_seed()

    if "export" in run_stages:
        stage_export()

    if "validate" in run_stages:
        stage_validate()

    print("\n✓ Pipeline complete.")


if __name__ == "__main__":
    main()
