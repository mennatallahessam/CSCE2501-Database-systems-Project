# CSCE 2501: Fundamentals of Database Systems — Project
## Resale Real Estate Database (Egypt Secondary Market)

A production-grade relational database and end-to-end data acquisition pipeline for Egypt's resale real-estate properties, based on [AqarExit](https://aqarexit.com/en/opportunities).

---

## 📑 Project Deliverables Directory

### Milestone I: Conceptual & Logical Database Design
| # | Deliverable | Location | Description |
|---|---|---|---|
| 1 | **Entity-Relationship Diagram (ERD)** | [`docs/milestone-1/ERD.md`](docs/milestone-1/ERD.md) | Formal ER specifications, entities, relationships, attributes, and Mermaid diagram |
| 2 | **Interactive ERD Visualization** | [`docs/milestone-1/ERD_Diagram.html`](docs/milestone-1/ERD_Diagram.html) | Interactive web-based SVG diagram with visual entity mapping |
| 3 | **ERD High-Resolution Screenshots** | [`docs/milestone-1/screenshots/`](docs/milestone-1/screenshots/) | Rendered PNG diagrams ([`erd_full.png`](docs/milestone-1/screenshots/erd_full.png), [`erd_top.png`](docs/milestone-1/screenshots/erd_top.png), [`erd_bottom.png`](docs/milestone-1/screenshots/erd_bottom.png)) |
| 4 | **Relational Model (Schema Mapping)** | [`docs/milestone-1/Relational_Model.md`](docs/milestone-1/Relational_Model.md) | 3NF / BCNF normalized schemas, functional dependencies, primary & foreign keys |
| 5 | **Relational Model (PDF Report)** | [`docs/milestone-1/Relational_Model.pdf`](docs/milestone-1/Relational_Model.pdf) | Submission-ready formatted PDF report |
| 6 | **Relational Model (Web View)** | [`docs/milestone-1/Relational_Model.html`](docs/milestone-1/Relational_Model.html) | Styled web presentation of the relational schemas |
| 7 | **MySQL Schema Transcript** | [`ResaleRealEstateDB.sql`](ResaleRealEstateDB.sql) | Complete DDL script creating all 9 tables, indexes, checks, and foreign keys |

### Milestone II: Web Crawler, ETL Pipeline & Database Population
| # | Deliverable | Location | Description |
|---|---|---|---|
| 1 | **Reconnaissance Report** | [`docs/milestone-2/RECON.md`](docs/milestone-2/RECON.md) | Platform architecture, robots.txt, rate limits, selectors, and schema mappings |
| 2 | **Master Pipeline Runner** | [`run_pipeline.py`](run_pipeline.py) | CLI runner managing discover, fetch, parse, clean, load, seed, export, validate |
| 3 | **Web Crawler Engine** | [`crawler/`](crawler/) | Resumable, rate-limited crawler (`discover.py`, `fetch.py`, `parse.py`) |
| 4 | **ETL & Data Transformation** | [`etl/`](etl/) | Cleaning, normalisation, MySQL idempotent loader, synthetic user seeding, CSV export |
| 5 | **Unit Test Suite** | [`tests/test_parse.py`](tests/test_parse.py) | 112 pytest cases validating Arabic extraction, regexes, and clean rules |
| 6 | **MySQL Database Dump** | [`output/resale_db_dump.sql`](output/resale_db_dump.sql) | Full database dump with 8,602 properties, 64,486 reviews, and utf8mb4 collation |
| 7 | **UTF-8 with BOM CSVs** | [`output/csv/`](output/csv/) | Clean CSV exports for all 9 tables matching database records 1-to-1 |
| 8 | **Validation Report** | [`docs/milestone-2/validation_report.md`](docs/milestone-2/validation_report.md) | Automated validation verifying 100% crawl completeness and zero orphan records |
| 9 | **Milestone III Smoke Tests** | [`validation/milestone3_smoke_tests.sql`](validation/milestone3_smoke_tests.sql) | 8 verified analytical SQL queries required for the application tier |

---

## 📂 Repository Structure

```text
csce2501-project-database/
├── README.md                           # Master project guide & deliverables index
├── ResaleRealEstateDB.sql              # Milestone I MySQL DDL schema script
├── config.py                           # Central configuration (crawler, db, paths)
├── requirements.txt                    # Python runtime dependencies
├── run_pipeline.py                     # Master CLI pipeline runner (stages 1-8)
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
│
├── docs/                               # Project documentation & deliverables
│   ├── milestone-1/                    # Milestone 1: ERD & Relational Model
│   │   ├── ERD.md                      # Conceptual design & Mermaid diagram
│   │   ├── ERD_Diagram.html            # Interactive SVG ERD viewer
│   │   ├── Relational_Model.md         # 3NF relational schemas & mapping proofs
│   │   ├── Relational_Model.html       # Styled HTML view of relational model
│   │   ├── Relational_Model.pdf        # Formatted PDF document
│   │   └── screenshots/                # Rendered PNG diagrams (full, top, bottom)
│   ├── milestone-2/                    # Milestone 2: Reconnaissance & Validation
│   │   ├── RECON.md                    # Target site analysis & field mapping
│   │   └── validation_report.md        # Pipeline data integrity & sanity report
│   └── specifications/                 # Course assignment instructions & prompts
│       ├── milestone_1_detailed_prompt.md
│       └── milestone2_prompt.md
│
├── crawler/                            # Stage 1-3: Web scraping modules
│   ├── discover.py                     # Sitemap parser (extracts property URLs)
│   ├── fetch.py                        # Polite, rate-limited HTTP fetcher
│   └── parse.py                        # BeautifulSoup & ld+json parser
│
├── etl/                                # Stage 4-7: Extraction, loading, and export
│   ├── clean.py                        # Field validation, cleaning & derived metrics
│   ├── load.py                         # Idempotent upsert loader for MySQL
│   ├── seed_users.py                   # Realistic Faker-based user & review seeding
│   └── export_csv.py                   # UTF-8 with BOM CSV exporter for all tables
│
├── output/                             # Exported deliverables
│   ├── resale_db_dump.sql              # Complete mysqldump SQL dump file
│   └── csv/                            # 9 exported CSV files matching all tables
│
├── samples/                            # Offline test fixtures & cached samples
│   ├── detail_*.html                   # Diverse property detail sample HTML pages
│   ├── property_urls.txt               # Enumerate listing URLs from sitemap
│   └── robots.txt                      # AqarExit robots.txt snapshot
│
├── scripts/                            # Helper utilities & reconnaissance tools
│   ├── generate_pdf.py                 # ReportLab script building Relational_Model.pdf
│   └── recon/                          # Phase 0 reconnaissance & probe scripts
│       ├── recon_probe.py              # Initial HTTP & headers probe
│       ├── recon_detail.py             # Sample detail page inspector
│       ├── inspect_html.py             # DOM & CSS class explorer
│       ├── extract_fields.py           # Structured ld+json & dl/dt extractor
│       └── print_ldjson.py             # Pretty-printer for JSON-LD schemas
│
├── tests/                              # Automated testing
│   └── test_parse.py                   # 112 pytest unit tests for parsing & cleaning
│
└── validation/                         # Stage 8: Data integrity & smoke tests
    ├── validate.py                     # Automated sanity & integrity validator
    └── milestone3_smoke_tests.sql      # Analytical queries for Milestone III
```

---

## 🏗️ Architecture & Pipeline Flow

```
[ AqarExit Sitemap ]
        │
        ▼ (Stage 1: discover)
[ samples/property_urls.txt (8,589 URLs) ]
        │
        ▼ (Stage 2: fetch — polite, rate-limited, resumable SQLite state)
[ raw/<slug>.html (Cached HTML responses) ]
        │
        ▼ (Stage 3 & 4: parse & clean)
[ Cleaned Property Records (Normalized vocabulary, derived fields) ]
        │
        ├──────────────────────────┐
        ▼ (Stage 5: load)          ▼ (Stage 6: seed)
  [ MySQL Non-User Tables ]    [ Synthetic User & Review Seeding ]
  (Location, Developer,        (200 users, realistic reviews, focus areas)
   Development, Property,
   Amenity, Property_Amenity)
        │                          │
        └─────────────┬────────────┘
                      ▼
        (Stage 7: export_csv)
  [ output/csv/*.csv (9 UTF-8-BOM tables) ]
                      │
                      ▼
        (Stage 8: validate)
  [ docs/milestone-2/validation_report.md & validation/milestone3_smoke_tests.sql ]
```

---

## ⚙️ Setup & Prerequisites

### 1. Environment & Dependencies

- **OS:** Windows / Linux / macOS
- **Python:** Python 3.11+
- **Database:** MySQL Server 8.0+

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials

Copy `.env.example` to `.env` and fill in your MySQL credentials:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=resalerealestatedb
DB_USER=root
DB_PASS=your_mysql_password
```

Initialize the database schema:
```bash
mysql -u root -p < ResaleRealEstateDB.sql
```

---

## 🚀 Running the Pipeline

### Run Full End-to-End Pipeline
```bash
python run_pipeline.py
```

### Run with a Page Fetch Limit (e.g. 50 properties for quick testing)
```bash
python run_pipeline.py --limit 50
```

### Run or Resume Specific Stages
```bash
# Skip directly to parsing and database loading (uses cached raw/ HTML)
python run_pipeline.py --start-stage parse

# Run ONLY the CSV export stage
python run_pipeline.py --only-stage export

# Run ONLY the data integrity validator
python run_pipeline.py --only-stage validate
```

---

## 🧪 Unit Testing

We provide a comprehensive pytest test suite validating all parsing routines, digit normalizations, Arabic regex extractors, and clean pipeline derivations across saved sample HTML files:

```bash
pytest tests/test_parse.py -v
```
*(All 112 tests pass cleanly with zero failures.)*

---

## 📐 Formulas for Derived Metrics

1. **Total Asking Price (`asking_price`)**:
   - For **installment** properties:
     $$\text{Total Asking Price} = \text{Down Payment (المطلوب كاش)} + \text{Remaining to Developer (المتبقي للمطور)}$$
   - For **cash** properties:
     $$\text{Total Asking Price} = \text{Cash Price (المطلوب كاش)}$$
2. **Price per Square Meter (`price_per_sqm`)**:
   $$\text{Price per m}^2 = \frac{\text{Total Asking Price}}{\text{Total Area (m}^2\text{)}}$$
   *(Guarded: area $> 0$, result must fall in realistic Egyptian real estate band $1,000 \le \text{EGP/m}^2 \le 5,000,000$).*
3. **Down Payment (`down_payment`)**:
   - Represents the immediate cash equity required to assume the contract:
     $$\text{Down Payment} = \text{Cash Required Now (المطلوب كاش دلوقتي)}$$
   - Guaranteed constraint: $\text{Down Payment} \le \text{Total Asking Price}$.
4. **Gain over Market (`gain_over_market`)**:
   $$\text{Gain \%} = \frac{\text{Gain EGP}}{\text{Total Asking Price}} \times 100$$
5. **Discount over Market (`discount_over_market`)**:
   $$\text{Discount \%} = \frac{\text{Market Price} - \text{Total Asking Price}}{\text{Market Price}} \times 100$$

---

## 💾 Database Dump & Clean Restore Verification

### Dump Command
```bash
mysqldump --single-transaction --routines --default-character-set=utf8mb4 -u root -p resalerealestatedb --result-file=output/resale_db_dump.sql
```

### Restore Verification Command
```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS test_restore_db; CREATE DATABASE test_restore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p --default-character-set=utf8mb4 test_restore_db < output/resale_db_dump.sql
mysql -u root -p -e "SHOW TABLES FROM test_restore_db;"
```
*(Verified: all 9 tables restore with identical row counts).*

---

## 🔍 Validation & Milestone III Support

- Post-load validation report is generated at [`docs/milestone-2/validation_report.md`](docs/milestone-2/validation_report.md).
- All 8 analytical queries required for Milestone III application layer are verified in [`validation/milestone3_smoke_tests.sql`](validation/milestone3_smoke_tests.sql).

---

## 👥 Course & Term

CSCE 2501: Fundamentals of Database Systems — AUC, Fall 2026