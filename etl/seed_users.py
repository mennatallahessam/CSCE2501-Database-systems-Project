# -*- coding: utf-8 -*-
"""
etl/seed_users.py
------------------
Generates synthetic User, Review and User_Focus_Area data.

Rules:
- Fixed random seed (SEED_RANDOM_SEED from config.py) → reproducible
- 200 users with consistent age/birthdate
- Focus areas drawn from actual crawled locations
- Reviews only on developments that exist in the DB
- One review per (user, development) — respects UNIQUE constraint
- Rating distribution skewed realistic (most 6-9, few 1-3 and 10)
- All data is synthetic — no real personal data
"""

import hashlib
import logging
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import mysql.connector
from faker import Faker

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER,
    NUM_REVIEWS_MAX, NUM_REVIEWS_MIN, NUM_USERS, SEED_RANDOM_SEED,
)

log = logging.getLogger(__name__)

faker = Faker("ar_EG")
faker_en = Faker("en_US")
random.seed(SEED_RANDOM_SEED)
Faker.seed(SEED_RANDOM_SEED)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fake_password(username: str) -> str:
    """Deterministic fake bcrypt-like hash (NOT a real hash — synthetic data only)."""
    return hashlib.sha256(f"synthetic_{username}_{SEED_RANDOM_SEED}".encode()).hexdigest()


def _random_birthdate(min_age: int = 18, max_age: int = 70) -> date:
    today = date.today()
    days = random.randint(min_age * 365, max_age * 365)
    return today - timedelta(days=days)


def _skewed_rating() -> int:
    """
    Realistic rating distribution:
        1-3: 10%, 4-5: 15%, 6-7: 30%, 8-9: 35%, 10: 10%
    """
    roll = random.random()
    if roll < 0.10:
        return random.randint(1, 3)
    elif roll < 0.25:
        return random.randint(4, 5)
    elif roll < 0.55:
        return random.randint(6, 7)
    elif roll < 0.90:
        return random.randint(8, 9)
    else:
        return 10


_REVIEW_TEMPLATES = [
    "المشروع ده تجربتي معاه كانت {adj}. الموقع {loc_adj} والخدمات {svc_adj}.",
    "شقة {adj} في مشروع {adj2}. السعر {price_adj} مقارنة بالمنطقة.",
    "تجربة {adj} بكل المقاييس — التسليم كان {delivery_adj}.",
    "المشروع بيوفّر {feat} وده نقطة قوية. بشكل عام {adj}.",
    "صاحبي اشترى هناك وكان {adj}. أنصح {recommend} المشروع ده.",
    "الأمن والخدمات {svc_adj}. التشطيبات {finish_adj}.",
]

_ADJ = ["ممتاز", "جيد جدًا", "مقبول", "رائع", "مميز", "عادي", "يحتاج تحسين"]
_LOC_ADJ = ["مميز", "مركزي", "هادي", "استراتيجي"]
_SVC_ADJ = ["عالية المستوى", "كويسة", "تحتاج تطوير", "ممتازة"]
_PRICE_ADJ = ["معقول", "مرتفع قليلًا", "منافس", "جيد"]
_DELIVERY_ADJ = ["في الموعد", "متأخر شوية", "قبل الموعد"]
_FEAT = ["حمام سباحة", "جيم", "أمن 24 ساعة", "كلوب هاوس", "مناطق خضراء"]
_FINISH_ADJ = ["ممتازة", "جيدة", "تحتاج مراجعة"]
_RECOMMEND = ["بشدة", "بشكل عام", "مع التحفظ على السعر"]


def _fake_review_text() -> str:
    template = random.choice(_REVIEW_TEMPLATES)
    return template.format(
        adj=random.choice(_ADJ),
        adj2=random.choice(_ADJ),
        loc_adj=random.choice(_LOC_ADJ),
        svc_adj=random.choice(_SVC_ADJ),
        price_adj=random.choice(_PRICE_ADJ),
        delivery_adj=random.choice(_DELIVERY_ADJ),
        feat=random.choice(_FEAT),
        finish_adj=random.choice(_FINISH_ADJ),
        recommend=random.choice(_RECOMMEND),
    )


# ── Database helpers ──────────────────────────────────────────────────────────

def _get_conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASS,
        charset="utf8mb4", collation="utf8mb4_unicode_ci", use_unicode=True,
    )


def _fetch_all_location_ids(conn) -> list[int]:
    cur = conn.cursor()
    cur.execute("SELECT location_id FROM Location")
    return [r[0] for r in cur.fetchall()]


def _fetch_all_development_ids(conn) -> list[int]:
    cur = conn.cursor()
    cur.execute("SELECT development_id FROM Development")
    return [r[0] for r in cur.fetchall()]


# ── Seed functions ────────────────────────────────────────────────────────────

def seed_users(conn, location_ids: list[int]) -> list[int]:
    """Insert NUM_USERS synthetic users; return their user_ids."""
    cur = conn.cursor()
    user_ids: list[int] = []
    used_emails: set[str] = set()
    used_usernames: set[str] = set()

    for _ in range(NUM_USERS):
        gender = random.choice(["Male", "Female"])
        birthdate = _random_birthdate()
        age = (date.today() - birthdate).days // 365

        # Unique username
        base = faker_en.user_name()
        username = base
        suffix = 1
        while username in used_usernames:
            username = f"{base}{suffix}"
            suffix += 1
        used_usernames.add(username)

        # Unique email
        email = faker_en.email()
        while email in used_emails:
            email = faker_en.email()
        used_emails.add(email)

        pw = _fake_password(username)

        cur.execute(
            """
            INSERT IGNORE INTO `User` (username, email, password_hash, gender, age, birthdate)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (username, email, pw, gender, age, birthdate.isoformat()),
        )
        if cur.lastrowid:
            user_ids.append(cur.lastrowid)

    conn.commit()
    log.info("Seeded %d users.", len(user_ids))

    # Fetch all user_ids (in case of ON DUPLICATE KEY)
    if not user_ids:
        cur.execute("SELECT user_id FROM `User`")
        user_ids = [r[0] for r in cur.fetchall()]

    # User_Focus_Area: each user picks 1-3 focus areas from real locations
    if location_ids:
        for uid in user_ids:
            n = random.randint(1, min(3, len(location_ids)))
            chosen = random.sample(location_ids, n)
            for lid in chosen:
                cur.execute(
                    "INSERT IGNORE INTO User_Focus_Area (user_id, location_id) VALUES (%s, %s)",
                    (uid, lid),
                )
        conn.commit()
        log.info("Seeded User_Focus_Area entries.")

    return user_ids


def seed_reviews(conn, user_ids: list[int], development_ids: list[int]) -> int:
    """
    Seed reviews: every development gets 3-10 reviews from random users.
    Respects the UNIQUE(user_id, development_id) constraint.
    """
    if not development_ids or not user_ids:
        log.warning("No developments or users — skipping review seeding.")
        return 0

    cur = conn.cursor()
    # Fetch existing user registration dates (use today as proxy)
    review_count = 0
    assigned: set[tuple[int, int]] = set()  # (user_id, dev_id)

    # Shuffle so distribution is random but reproducible
    devs = list(development_ids)
    random.shuffle(devs)

    for dev_id in devs:
        n = random.randint(NUM_REVIEWS_MIN, min(NUM_REVIEWS_MAX, len(user_ids)))
        reviewers = random.sample(user_ids, n)
        for uid in reviewers:
            pair = (uid, dev_id)
            if pair in assigned:
                continue
            assigned.add(pair)

            rating = _skewed_rating()
            text = _fake_review_text()
            # Review date: random date in the last 3 years
            days_ago = random.randint(1, 1095)
            review_date = (date.today() - timedelta(days=days_ago)).isoformat()

            cur.execute(
                """
                INSERT IGNORE INTO Review
                    (user_id, development_id, rating, review_comment, review_date)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (uid, dev_id, rating, text, review_date),
            )
            review_count += 1

    conn.commit()
    log.info("Seeded %d reviews across %d developments.", review_count, len(devs))
    return review_count


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    print("Connecting to database…")
    conn = _get_conn()

    location_ids = _fetch_all_location_ids(conn)
    development_ids = _fetch_all_development_ids(conn)

    print(f"Found {len(location_ids)} locations and {len(development_ids)} developments.")

    user_ids = seed_users(conn, location_ids)
    print(f"Seeded {len(user_ids)} users.")

    review_count = seed_reviews(conn, user_ids, development_ids)
    print(f"Seeded {review_count} reviews.")

    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
