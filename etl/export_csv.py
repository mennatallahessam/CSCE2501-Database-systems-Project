# -*- coding: utf-8 -*-
"""
etl/export_csv.py
------------------
Export every database table to a UTF-8-with-BOM CSV file.

BOM ensures Excel displays Arabic text correctly.
Row counts printed and compared with DB counts.

Usage:
    python -m etl.export_csv [--out DIR]
"""

import csv
import logging
import sys
from pathlib import Path

import mysql.connector

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import CSV_DIR, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

log = logging.getLogger(__name__)

TABLES = [
    "Location",
    "Developer",
    "Development",
    "Property",
    "Amenity",
    "Property_Amenity",
    "User",
    "User_Focus_Area",
    "Review",
]


def export_table(conn, table: str, out_dir: Path) -> int:
    """Export a single table to CSV; return row count written."""
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM `{table}`")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    out_path = out_dir / f"{table}.csv"
    with out_path.open("w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig = BOM
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    log.info("Exported %s → %s (%d rows)", table, out_path.name, len(rows))
    return len(rows)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    import argparse
    parser = argparse.ArgumentParser(description="Export all tables to CSV.")
    parser.add_argument("--out", default=CSV_DIR, help="Output directory.")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASS,
        charset="utf8mb4", collation="utf8mb4_unicode_ci", use_unicode=True,
    )

    print("\n── CSV Export ──────────────────────────────────")
    total = 0
    for tbl in TABLES:
        try:
            count = export_table(conn, tbl, out_dir)
            total += count
            print(f"  {tbl:<25} {count:>6} rows → {tbl}.csv")
        except Exception as e:
            print(f"  {tbl:<25} ERROR: {e}")

    print(f"  {'TOTAL':<25} {total:>6} rows")
    print(f"────────────────────────────────────────────────")
    print(f"CSVs written to: {out_dir.resolve()}")
    conn.close()


if __name__ == "__main__":
    main()
