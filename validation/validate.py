# -*- coding: utf-8 -*-
"""
validation/validate.py
-----------------------
Post-load integrity and quality report.

Generates validation_report.md (printed and saved).

Checks:
1. Completeness: crawled vs total discovered
2. Row counts per table and CSV vs DB agreement
3. Integrity: orphan FKs, duplicate natural keys, schema violations
4. NULL rate per column in Property table
5. Sanity checks: price ranges, area > 0, down_payment <= price, ratings 1-10
6. Spot check: 10 random properties raw vs stored
"""

import csv
import logging
import os
import random
import sys
from pathlib import Path
from datetime import date

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mysql.connector

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    CSV_DIR, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER,
    STATE_DB,
)

log = logging.getLogger(__name__)
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "milestone-2" / "validation_report.md"


def _conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASS,
        charset="utf8mb4", use_unicode=True,
    )


def _q(conn, sql, params=()) -> list:
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur.fetchall()


# ── Report builder ────────────────────────────────────────────────────────────

class Report:
    def __init__(self):
        self.lines: list[str] = []

    def h(self, title: str, level: int = 2):
        prefix = "#" * level
        self.lines.append(f"\n{prefix} {title}\n")

    def p(self, text: str):
        self.lines.append(text)

    def table(self, headers: list[str], rows: list[list]):
        self.lines.append("| " + " | ".join(str(h) for h in headers) + " |")
        self.lines.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in rows:
            self.lines.append("| " + " | ".join(str(c) for c in row) + " |")

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.lines), encoding="utf-8")
        print(f"\nValidation report saved → {path}")


# ── Checks ────────────────────────────────────────────────────────────────────

def check_completeness(report: Report) -> None:
    report.h("1. Crawl Completeness", 2)

    url_file = Path("./samples/property_urls.txt")
    total_discovered = 0
    if url_file.exists():
        total_discovered = len(url_file.read_text("utf-8").splitlines())

    import sqlite3
    state_db = Path(STATE_DB)
    total_done = total_failed = total_pending = 0
    if state_db.exists():
        sconn = sqlite3.connect(str(state_db))
        total_done = sconn.execute("SELECT COUNT(*) FROM crawl_state WHERE status='done'").fetchone()[0]
        total_failed = sconn.execute("SELECT COUNT(*) FROM crawl_state WHERE status='failed'").fetchone()[0]
        total_pending = sconn.execute("SELECT COUNT(*) FROM crawl_state WHERE status='pending'").fetchone()[0]
        sconn.close()

    report.p(f"- **Total discovered in sitemap:** {total_discovered}")
    report.p(f"- **Crawled (done):** {total_done} ({100*total_done//max(total_discovered,1)}%)")
    report.p(f"- **Failed:** {total_failed}")
    report.p(f"- **Pending:** {total_pending}")

    if total_failed > 0:
        report.p(f"\n> [!WARNING]\n> {total_failed} URLs failed. Check crawl.log for details.")


def check_row_counts(conn, report: Report) -> dict[str, int]:
    report.h("2. Row Counts per Table", 2)
    tables = [
        "Location", "Developer", "Development", "Property",
        "Amenity", "Property_Amenity", "User", "User_Focus_Area", "Review",
    ]
    db_counts: dict[str, int] = {}
    rows = []
    for tbl in tables:
        try:
            result = _q(conn, f"SELECT COUNT(*) FROM `{tbl}`")
            count = result[0][0] if result else 0
        except Exception as e:
            count = -1
            log.warning("Could not count %s: %s", tbl, e)
        db_counts[tbl] = count

        # CSV count
        csv_path = Path(CSV_DIR) / f"{tbl}.csv"
        csv_count = "N/A"
        match_symbol = "—"
        if csv_path.exists():
            with open(csv_path, encoding="utf-8-sig") as f:
                csv_count = sum(1 for _ in f) - 1  # minus header
            match_symbol = "✓" if csv_count == count else "✗ MISMATCH"

        rows.append([tbl, count, csv_count, match_symbol])

    report.table(["Table", "DB Rows", "CSV Rows", "Match"], rows)
    return db_counts


def check_integrity(conn, report: Report) -> None:
    report.h("3. Integrity Checks", 2)
    checks = [
        ("Orphan Property → Development", """
            SELECT COUNT(*) FROM Property p
            WHERE p.development_id IS NOT NULL
              AND NOT EXISTS (SELECT 1 FROM Development d WHERE d.development_id = p.development_id)
        """),
        ("Orphan Property → Location", """
            SELECT COUNT(*) FROM Property p
            WHERE p.location_id IS NOT NULL
              AND NOT EXISTS (SELECT 1 FROM Location l WHERE l.location_id = p.location_id)
        """),
        ("Orphan Development → Developer", """
            SELECT COUNT(*) FROM Development d
            WHERE NOT EXISTS (SELECT 1 FROM Developer dev WHERE dev.developer_id = d.developer_id)
        """),
        ("Orphan Review → User", """
            SELECT COUNT(*) FROM Review r
            WHERE NOT EXISTS (SELECT 1 FROM `User` u WHERE u.user_id = r.user_id)
        """),
        ("Orphan Review → Development", """
            SELECT COUNT(*) FROM Review r
            WHERE NOT EXISTS (SELECT 1 FROM Development d WHERE d.development_id = r.development_id)
        """),
        ("Duplicate source_url in Property", """
            SELECT COUNT(*) - COUNT(DISTINCT source_url) FROM Property
        """),
    ]
    rows = []
    for label, sql in checks:
        try:
            result = _q(conn, sql)
            val = result[0][0] if result else "ERR"
            status = "✓ OK" if val == 0 else f"✗ {val} violations"
        except Exception as e:
            status = f"ERR: {e}"
        rows.append([label, status])
    report.table(["Check", "Result"], rows)


def check_null_rates(conn, report: Report) -> None:
    report.h("4. NULL Rate per Column (Property table)", 2)
    columns = [
        "title", "description", "total_area_sqm", "num_bedrooms", "num_bathrooms",
        "property_type", "asking_price", "price_per_sqm", "payment_method",
        "down_payment", "contract_year", "gain_over_market", "discount_over_market",
        "development_id", "location_id",
    ]
    total = _q(conn, "SELECT COUNT(*) FROM Property")[0][0]
    if total == 0:
        report.p("No properties loaded yet.")
        return

    rows = []
    for col in columns:
        try:
            null_count = _q(conn, f"SELECT COUNT(*) FROM Property WHERE `{col}` IS NULL")[0][0]
            pct = round(100 * null_count / total, 1)
            flag = "⚠️" if pct > 50 else ""
            rows.append([col, null_count, f"{pct}%", flag])
        except Exception as e:
            rows.append([col, "ERR", "ERR", str(e)])

    report.table(["Column", "NULL count", "NULL %", "Flag"], rows)


def check_sanity(conn, report: Report) -> None:
    report.h("5. Sanity Checks", 2)

    checks = [
        ("Properties with area ≤ 0", "SELECT COUNT(*) FROM Property WHERE total_area_sqm <= 0"),
        ("Properties with asking_price < 0", "SELECT COUNT(*) FROM Property WHERE asking_price < 0"),
        ("Properties with down_payment > asking_price",
         "SELECT COUNT(*) FROM Property WHERE down_payment IS NOT NULL AND asking_price IS NOT NULL AND down_payment > asking_price"),
        ("Properties with price_per_sqm > 5,000,000", "SELECT COUNT(*) FROM Property WHERE price_per_sqm > 5000000"),
        ("Properties with price_per_sqm < 1,000", "SELECT COUNT(*) FROM Property WHERE price_per_sqm < 1000 AND price_per_sqm IS NOT NULL"),
        ("Reviews with rating outside 1-10", "SELECT COUNT(*) FROM Review WHERE rating < 1 OR rating > 10"),
        ("Users with age < 18", "SELECT COUNT(*) FROM `User` WHERE age < 18"),
        ("Properties without development_id assigned",
         "SELECT COUNT(*) FROM Property WHERE development_id IS NULL"),
    ]
    rows = []
    for label, sql in checks:
        try:
            val = _q(conn, sql)[0][0]
            status = "✓ OK" if val == 0 else f"⚠️ {val}"
        except Exception as e:
            status = f"ERR: {e}"
        rows.append([label, status])
    report.table(["Check", "Result"], rows)


def spot_check(conn, report: Report) -> None:
    report.h("6. Spot Check — 10 Random Properties", 2)
    report.p("*Compare these against live site manually.*\n")

    try:
        props = _q(conn, """
            SELECT p.property_id, p.title, p.source_url, p.total_area_sqm,
                   p.num_bedrooms, p.asking_price, p.property_type,
                   p.price_per_sqm, p.gain_over_market,
                   d.project_name, dev.developer_name, l.area_name
            FROM Property p
            LEFT JOIN Development d ON p.development_id = d.development_id
            LEFT JOIN Developer dev ON d.developer_id = dev.developer_id
            LEFT JOIN Location l ON p.location_id = l.location_id
            ORDER BY RAND()
            LIMIT 10
        """)
    except Exception as e:
        report.p(f"Error: {e}")
        return

    if not props:
        report.p("No properties in DB yet.")
        return

    headers = ["ID", "Title", "Area m²", "Beds", "Price EGP", "Type", "EGP/m²", "Gain%", "Project", "Developer", "Location", "URL"]
    rows = []
    for row in props:
        pid, title, url, area, beds, price, ptype, ppsm, gain, proj, dev, loc = row
        rows.append([
            pid,
            (title or "")[:40],
            area,
            beds,
            f"{price:,.0f}" if price else "NULL",
            ptype,
            f"{ppsm:,.0f}" if ppsm else "NULL",
            f"{gain}%" if gain else "NULL",
            (proj or "")[:30],
            (dev or "")[:30],
            loc,
            (url or "")[-50:],
        ])
    report.table(headers, rows)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    report = Report()
    report.lines.append("# AqarExit Database Validation Report\n")
    report.lines.append(f"*Generated: {date.today().isoformat()}*\n")
    report.lines.append("> [!NOTE]\n> This report is auto-generated by validation/validate.py\n")

    conn = _conn()

    check_completeness(report)
    check_row_counts(conn, report)
    check_integrity(conn, report)
    check_null_rates(conn, report)
    check_sanity(conn, report)
    spot_check(conn, report)

    conn.close()

    print("\n".join(report.lines))
    report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
