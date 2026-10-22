# AqarExit Crawler — Configuration
# All tuneable settings live here. Override with environment variables if needed.

import os
from dotenv import load_dotenv

load_dotenv()

# ── Crawl politeness ────────────────────────────────────────────────────────
DELAY_MIN: float = 2.0          # seconds between requests (minimum)
DELAY_MAX: float = 4.0          # seconds between requests (maximum)
MAX_RETRIES: int = 5            # attempts per URL before marking as failed
BACKOFF_BASE: float = 2.0       # exponential backoff multiplier (seconds)
REQUEST_TIMEOUT: int = 25       # HTTP timeout in seconds
CIRCUIT_BREAK_THRESHOLD: int = 10  # consecutive hard errors before stopping

# ── User-Agent ───────────────────────────────────────────────────────────────
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 "
    "(student project, CSCE 2501 AUC - non-commercial crawl)"
)

# ── URLs ─────────────────────────────────────────────────────────────────────
BASE_URL = "https://aqarexit.com"
SITEMAP_URL = "https://aqarexit.com/sitemap.xml"

# ── Paths ────────────────────────────────────────────────────────────────────
RAW_DIR = "./raw"
SAMPLES_DIR = "./samples"
OUTPUT_DIR = "./output"
CSV_DIR = "./output/csv"
LOG_FILE = "./crawl.log"
STATE_DB = "./crawl_state.sqlite"

# ── Database ─────────────────────────────────────────────────────────────────
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "ResaleRealEstateDB")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")

# ── Seeding ──────────────────────────────────────────────────────────────────
SEED_RANDOM_SEED = 42
NUM_USERS = 200
NUM_REVIEWS_MIN = 3   # per development
NUM_REVIEWS_MAX = 10
