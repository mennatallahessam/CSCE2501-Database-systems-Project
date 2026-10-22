# -*- coding: utf-8 -*-
"""
etl/load.py
-----------
Idempotent MySQL loader.

Load order respects foreign keys:
  Location → Developer → Development → Property → Property_Amenity (+ Amenity)

All inserts use INSERT ... ON DUPLICATE KEY UPDATE on natural keys so
re-running never creates duplicate rows.

Credentials are read from environment variables via config.py (never hardcoded).
"""

import logging
import sys
from pathlib import Path
from typing import Any

import mysql.connector
from mysql.connector import MySQLConnection

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

log = logging.getLogger(__name__)


# ── Connection ────────────────────────────────────────────────────────────────

def get_connection() -> MySQLConnection:
    """Return an open MySQL connection using config.py credentials."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        use_unicode=True,
    )
    conn.autocommit = False
    return conn


# ── Generic upsert helpers ────────────────────────────────────────────────────

def _upsert_location(cur, city: str | None, district: str | None,
                      area_name: str | None, compound_name: str | None) -> int | None:
    """Upsert a Location row; return its location_id (truly idempotent)."""
    target_city = city or area_name or "Cairo"
    cur.execute(
        """
        SELECT location_id FROM Location 
        WHERE city <=> %s AND district <=> %s AND area_name <=> %s AND compound_name <=> %s 
        LIMIT 1
        """,
        (target_city, district, area_name, compound_name),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO Location (city, district, area_name, compound_name)
        VALUES (%s, %s, %s, %s)
        """,
        (target_city, district, area_name, compound_name),
    )
    return cur.lastrowid


def _upsert_developer(cur, developer_name: str) -> int | None:
    """Upsert a Developer row; return its developer_id."""
    if not developer_name:
        return None
    cur.execute(
        """
        INSERT INTO Developer (developer_name)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE developer_name = developer_name
        """,
        (developer_name,),
    )
    if cur.lastrowid and cur.lastrowid != 0:
        return cur.lastrowid
    cur.execute(
        "SELECT developer_id FROM Developer WHERE developer_name=%s LIMIT 1",
        (developer_name,),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _upsert_development(cur, project_name: str, developer_id: int | None,
                          location_id: int | None) -> int | None:
    """Upsert a Development row; return its development_id."""
    if not project_name or not developer_id or not location_id:
        return None
    cur.execute(
        "SELECT development_id FROM Development WHERE project_name=%s AND developer_id=%s LIMIT 1",
        (project_name, developer_id),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO Development (project_name, developer_id, location_id)
        VALUES (%s, %s, %s)
        """,
        (project_name, developer_id, location_id),
    )
    return cur.lastrowid


def _upsert_amenity(cur, amenity_name: str) -> int | None:
    """Upsert an Amenity row; return amenity_id."""
    if not amenity_name:
        return None
    cur.execute(
        """
        INSERT INTO Amenity (amenity_name)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE amenity_name = amenity_name
        """,
        (amenity_name,),
    )
    if cur.lastrowid and cur.lastrowid != 0:
        return cur.lastrowid
    cur.execute(
        "SELECT amenity_id FROM Amenity WHERE amenity_name=%s LIMIT 1",
        (amenity_name,),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _upsert_property(cur, data: dict[str, Any], development_id: int | None,
                      location_id: int | None) -> int | None:
    """Upsert a Property row using source_url as the natural key."""
    source_url = data.get("source_url")
    title = (data.get("title") or "")[:255]
    description = data.get("description")
    total_area_sqm = data.get("total_area_sqm")
    num_bedrooms = data.get("num_bedrooms")
    num_bathrooms = data.get("num_bathrooms")
    property_type = data.get("property_type") or "other"
    asking_price = data.get("asking_price")
    price_per_sqm = data.get("price_per_sqm")
    payment_method = data.get("payment_method") or "cash"
    down_payment = data.get("down_payment")
    contract_year = data.get("contract_year")
    discount_over_market = data.get("discount_over_market")
    gain_over_market = data.get("gain_over_market")

    if source_url:
        cur.execute("SELECT property_id FROM Property WHERE source_url=%s LIMIT 1", (source_url,))
        row = cur.fetchone()
        if row:
            prop_id = row[0]
            cur.execute(
                """
                UPDATE Property SET
                    title = %s, description = %s, total_area_sqm = %s,
                    num_bedrooms = %s, num_bathrooms = %s, property_type = %s,
                    asking_price = %s, price_per_sqm = %s, payment_method = %s,
                    down_payment = %s, contract_year = %s, discount_over_market = %s,
                    gain_over_market = %s, development_id = %s, location_id = %s
                WHERE property_id = %s
                """,
                (
                    title, description, total_area_sqm,
                    num_bedrooms, num_bathrooms, property_type,
                    asking_price, price_per_sqm, payment_method,
                    down_payment, contract_year, discount_over_market,
                    gain_over_market, development_id, location_id,
                    prop_id,
                ),
            )
            return prop_id

    cur.execute(
        """
        INSERT INTO Property (
            title, description, source_url,
            total_area_sqm, num_bedrooms, num_bathrooms,
            property_type, asking_price, price_per_sqm,
            payment_method, down_payment, contract_year,
            discount_over_market, gain_over_market,
            development_id, location_id
        ) VALUES (
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s
        )
        """,
        (
            title, description, source_url,
            total_area_sqm, num_bedrooms, num_bathrooms,
            property_type, asking_price, price_per_sqm,
            payment_method, down_payment, contract_year,
            discount_over_market, gain_over_market,
            development_id, location_id,
        ),
    )
    return cur.lastrowid


# ── Main load function ────────────────────────────────────────────────────────

def load_property(conn: MySQLConnection, data: dict[str, Any]) -> bool:
    """
    Load a single cleaned property record (and all its dependents) into MySQL.

    Returns True on success, False on failure (rolls back on error).
    """
    try:
        cur = conn.cursor()

        # 1. Location
        location_id = _upsert_location(
            cur,
            city=data.get("city"),
            district=data.get("district"),
            area_name=data.get("area_name"),
            compound_name=data.get("compound_name"),
        )

        # 2. Developer
        developer_id = _upsert_developer(cur, data.get("developer_name") or "")

        # 3. Development
        development_id = _upsert_development(
            cur,
            project_name=data.get("project_name") or "",
            developer_id=developer_id,
            location_id=location_id,
        )

        # 4. Property
        property_id = _upsert_property(cur, data, development_id, location_id)

        # 5. Amenities (junction table)
        if property_id:
            for amenity_name in data.get("amenities") or []:
                amenity_id = _upsert_amenity(cur, amenity_name)
                if amenity_id:
                    cur.execute(
                        """
                        INSERT IGNORE INTO Property_Amenity (property_id, amenity_id)
                        VALUES (%s, %s)
                        """,
                        (property_id, amenity_id),
                    )

        conn.commit()
        return True

    except Exception as exc:
        conn.rollback()
        log.error("Failed to load property %s: %s", data.get("source_url"), exc)
        return False


def load_all(records: list[dict[str, Any]]) -> tuple[int, int]:
    """
    Load a list of cleaned property records.

    Returns (success_count, failure_count).
    """
    conn = get_connection()
    ok, fail = 0, 0
    for i, rec in enumerate(records):
        if load_property(conn, rec):
            ok += 1
        else:
            fail += 1
        if (i + 1) % 100 == 0:
            log.info("Loaded %d/%d  ok=%d fail=%d", i + 1, len(records), ok, fail)
    conn.close()
    log.info("Load complete: ok=%d  fail=%d", ok, fail)
    return ok, fail


def print_row_counts(conn: MySQLConnection) -> None:
    """Print row counts for every table in the schema."""
    tables = [
        "Location", "Developer", "Development", "Property",
        "Amenity", "Property_Amenity", "User", "User_Focus_Area", "Review",
    ]
    cur = conn.cursor()
    print("\n── Row counts ──────────────────────────────────")
    for tbl in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM `{tbl}`")
            row = cur.fetchone()
            count = row[0] if row else "ERR"
        except Exception as e:
            count = f"ERR({e})"
        print(f"  {tbl:<20} {count:>6}")
    print("────────────────────────────────────────────────\n")
