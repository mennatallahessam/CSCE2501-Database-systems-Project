# CSCE 2501: Fundamentals of Database Systems — Project
## Resale Real Estate Database & Data Pipeline (Egypt Secondary Market)

A production-grade relational database and end-to-end data acquisition pipeline modeling Egypt's resale real-estate secondary market, built on top of [AqarExit](https://aqarexit.com/en/opportunities).

---

## 📑 Project Deliverables Directory

### Milestone I: Conceptual & Logical Database Design
| # | Deliverable | Location | Description |
|---|---|---|---|
| 1 | **Entity-Relationship Diagram (ERD)** | [`docs/milestone-1/ERD.md`](docs/milestone-1/ERD.md) | Formal conceptual ER specifications, entities, relationships, cardinalities, and Mermaid diagram |
| 2 | **Interactive ERD Visualization** | [`docs/milestone-1/ERD_Diagram.html`](docs/milestone-1/ERD_Diagram.html) | Interactive web-based SVG diagram with visual entity mapping and relationships |
| 3 | **ERD High-Resolution Screenshots** | [`docs/milestone-1/screenshots/`](docs/milestone-1/screenshots/) | Rendered high-res PNG diagrams ([`erd_full.png`](docs/milestone-1/screenshots/erd_full.png), [`erd_top.png`](docs/milestone-1/screenshots/erd_top.png), [`erd_bottom.png`](docs/milestone-1/screenshots/erd_bottom.png)) |
| 4 | **Relational Model (Schema Mapping)** | [`docs/milestone-1/Relational_Model.md`](docs/milestone-1/Relational_Model.md) | 3NF / BCNF normalized schemas, functional dependencies, primary & foreign keys, constraint proofs |
| 5 | **Relational Model (PDF Report)** | [`docs/milestone-1/Relational_Model.pdf`](docs/milestone-1/Relational_Model.pdf) | Formatted, publication-ready PDF submission report |
| 6 | **Relational Model (Web View)** | [`docs/milestone-1/Relational_Model.html`](docs/milestone-1/Relational_Model.html) | Responsive, styled HTML presentation of all relational schemas |
| 7 | **MySQL DDL Schema Script** | [`ResaleRealEstateDB.sql`](ResaleRealEstateDB.sql) | Complete DDL script creating all 9 tables, indexes, checks, and foreign keys |

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

## 🎯 Domain Context & Market Dynamics

Unlike primary (off-plan) markets where buyers purchase directly from real estate developers under uniform payment plans, Egypt's **resale (secondary) market** presents distinct transactional complexities:
1. **Contract Assumption & Equity ("المطلوب كاش دلوقتي")**: Resale transactions require buyers to pay the seller's accumulated equity as an upfront cash down payment.
2. **Remaining Developer Debt ("المتبقي للمطور")**: The buyer assumes remaining installment schedules owed to the original master developer, paid over varying frequencies (monthly, quarterly, semi-annually).
3. **Total Asking Price Composition**:
   - For **installment** properties: $\text{Total Asking Price} = \text{Down Payment (Cash Now)} + \text{Remaining to Developer}$.
   - For **cash** properties: $\text{Total Asking Price} = \text{Cash Required Now}$.
4. **Market Arbitrage Metrics**: Properties frequently trade at discounts or premiums relative to current developer prices, represented by **Gain over Market** (`gain_over_market`) and **Discount over Market** (`discount_over_market`).

This database models these complex multi-tiered financial flows, developmental relationships, physical specifications, amenities, and user engagement reviews.

---

## 🗄️ Relational Schema Design (Milestone I)

The database schema is strictly normalized to **Boyce-Codd Normal Form (BCNF) / Third Normal Form (3NF)** and consists of **9 tables**:

```
 ┌──────────────┐         ┌───────────────┐
 │   Developer  │ 1     N │  Development  │ 1     N ┌──────────────┐
 │──────────────│─────────│───────────────│─────────│   Property   │
 │ developer_id │         │development_id │         │──────────────│
 └──────────────┘         └───────┬───────┘         │ property_id  │
                                  │                 └──────┬───────┘
                                  │ N                      │ M
                                  ▼ 1                      ▼ N
                           ┌──────────────┐         ┌───────────────────┐
                           │   Location   │         │ Property_Amenity  │
                           │──────────────│         │───────────────────│
                           │ location_id  │         │(prop_id, amen_id) │
                           └──────────────┘         └─────────┬─────────┘
                                  ▲ 1                         │ N
                                  │                           ▼ 1
                                  │ M                   ┌──────────────┐
                           ┌──────────────┐             │   Amenity    │
                           │User_Focus_Area             │──────────────│
                           │──────────────│             │  amenity_id  │
                           │(usr_id,loc_id)             └──────────────┘
                           └──────┬───────┘
                                  │ M
                                  ▼ 1
                           ┌──────────────┐ 1     N ┌──────────────┐
                           │     User     │─────────│    Review    │
                           │──────────────│         │──────────────│
                           │   user_id    │         │  review_id   │
                           └──────────────┘         └──────────────┘
```

### Table Breakdown & Specifications

#### 1. Independent Lookup & Master Tables
- **`Location`** (`location_id` [PK], `city`, `district`, `area_name`, `compound_name`):
  - Captures geographical hierarchy across Egyptian governorates, cities, and specific compounds.
  - Normalized without cycles; independent entity.
- **`Developer`** (`developer_id` [PK], `developer_name` [UNIQUE], `corporate_details`, `total_projects`, `total_properties_listed`):
  - Master entity for real estate development firms (e.g., Talaat Moustafa Group, Emaar Misr, Palm Hills, Hassan Allam, SODIC).
- **`Amenity`** (`amenity_id` [PK], `amenity_name` [UNIQUE]):
  - Normalized lookup table for distinct property amenities (e.g., Swimming Pool, Gym, Private Garden, Security, Covered Parking).
- **`User`** (`user_id` [PK], `username` [UNIQUE], `email` [UNIQUE], `password_hash`, `gender`, `age`, `birthdate`):
  - User accounts supporting authentication and demographic profiling.
  - Domain constraints: `CHECK (gender IN ('Male', 'Female'))`, `CHECK (age >= 18)`.

#### 2. Dependent Entity Tables
- **`Development`** (`development_id` [PK], `project_name`, `description`, `developer_id` [FK], `location_id` [FK]):
  - Master compound or project entity.
  - Foreign keys: references `Developer` and `Location` with `ON DELETE RESTRICT ON UPDATE CASCADE`.
- **`Property`** (`property_id` [PK], `title`, `description`, `source_url`, `total_area_sqm`, `num_bedrooms`, `num_bathrooms`, `property_type`, `asking_price`, `price_per_sqm`, `payment_method`, `down_payment`, `contract_year`, `discount_over_market`, `gain_over_market`, `development_id` [FK], `location_id` [FK]):
  - Core transactional listing table capturing physical specifications, financials, and URLs.
  - Foreign keys: references `Development` (`ON DELETE CASCADE`) and `Location` (`ON DELETE RESTRICT`).
  - Domain checks:
    - `property_type IN ('apartment', 'villa', 'townhouse', 'duplex', 'chalet', 'penthouse', 'studio', 'other')`
    - `payment_method IN ('cash', 'installment')`
    - `num_bedrooms >= 0`, `num_bathrooms >= 0`, `total_area_sqm > 0`, `asking_price >= 0`

#### 3. Associative (Junction) & Interaction Tables
- **`Property_Amenity`** (`property_id` [PK, FK], `amenity_id` [PK, FK]):
  - Resolves M:N relationship between properties and amenities.
  - Cascading deletes on both foreign keys.
- **`User_Focus_Area`** (`user_id` [PK, FK], `location_id` [PK, FK]):
  - Resolves M:N relationship between registered users and their geographic areas of interest.
  - Cascading deletes on both foreign keys.
- **`Review`** (`review_id` [PK], `user_id` [FK], `development_id` [FK], `rating`, `review_comment`, `review_date`):
  - Captures user evaluations for specific development projects.
  - Constraints: `UNIQUE (user_id, development_id)` guarantees at most one review per user per project; `CHECK (rating BETWEEN 1 AND 10)`.

---

## 🏗️ End-to-End Pipeline Architecture (Milestone II)

The data pipeline is designed with strict separation of concerns, complete decoupling of network acquisition from parsing, full idempotency, and automated data validation.

```
                  ┌───────────────────────────────┐
                  │ AqarExit XML Sitemap (8,589)  │
                  └───────────────┬───────────────┘
                                  │
                                  ▼ (Stage 1: discover)
                  ┌───────────────────────────────┐
                  │   samples/property_urls.txt   │
                  └───────────────┬───────────────┘
                                  │
                                  ▼ (Stage 2: fetch)
                  ┌───────────────────────────────┐
                  │ Polite Rate-Limited Crawler   │ ◄─── SQLite State Engine
                  │ Jitter (2-4s), Backoff, Jails │      (crawl_state.sqlite)
                  └───────────────┬───────────────┘
                                  │
                                  ▼ (Offline Disk Caching)
                  ┌───────────────────────────────┐
                  │ raw/<property_uuid>.html      │
                  └───────────────┬───────────────┘
                                  │
                                  ▼ (Stage 3 & 4: parse & clean)
                  ┌───────────────────────────────┐
                  │ Pure Function Parser & Clean  │ ◄─── 112 Pytest Unit Tests
                  │ Arabic Normalization & Rules  │      (tests/test_parse.py)
                  └───────┬───────────────┬───────┘
                          │               │
                          ▼ (Stage 5)     ▼ (Stage 6)
                  ┌───────────────┐ ┌───────────────────┐
                  │  MySQL Loader │ │ Synthetic Seeding │
                  │  (Idempotent  │ │ 200 Users, Faker  │
                  │   Upserts)    │ │ 64k+ Project Revs │
                  └───────┬───────┘ └─────────┬─────────┘
                          │                   │
                          └─────────┬─────────┘
                                    │
                                    ▼ (Stage 7: export_csv)
                  ┌───────────────────────────────────┐
                  │ output/csv/*.csv (9 UTF-8-BOM)   │
                  └─────────────────┬─────────────────┘
                                    │
                                    ▼ (Stage 8: validate)
                  ┌───────────────────────────────────┐
                  │ Automated Sanity & Validation     │
                  │ docs/milestone-2/validation_report│
                  └───────────────────────────────────┘
```

### Pipeline Stages Overview

| Stage | Name | Key Function / Module | Description |
|---|---|---|---|
| **1** | `discover` | [`crawler/discover.py`](crawler/discover.py) | Downloads and parses XML sitemap, extracting all 8,589 canonical property URLs. |
| **2** | `fetch` | [`crawler/fetch.py`](crawler/fetch.py) | Polite HTTP crawler with randomized delay (2–4s), persistent sessions, exponential backoff, and SQLite state tracking. Caches raw HTML to `raw/`. |
| **3** | `parse` | [`crawler/parse.py`](crawler/parse.py) | Pure-function parser extracting JSON-LD (`application/ld+json`), `<dl>` definitions, and Arabic text patterns. |
| **4** | `clean` | [`etl/clean.py`](etl/clean.py) | Normalizes Arabic-Indic digits, standardizes property types, reconciles locations, and computes derived financial metrics. |
| **5** | `load` | [`etl/load.py`](etl/load.py) | Idempotent upsert loader inserting data into MySQL in dependency order using `INSERT ... ON DUPLICATE KEY UPDATE`. |
| **6** | `seed` | [`etl/seed_users.py`](etl/seed_users.py) | Generates 200 realistic users and 64,486 synthetic reviews using Faker (`ar_EG` / `en_US`) with deterministic seeding (`SEED_RANDOM_SEED = 42`). |
| **7** | `export` | [`etl/export_csv.py`](etl/export_csv.py) | Exports all 9 MySQL tables to UTF-8 with BOM (`utf-8-sig`) CSV files for guaranteed Excel compatibility. |
| **8** | `validate`| [`validation/validate.py`](validation/validate.py) | Runs complete referential integrity, orphan checks, NULL-rate analysis, and sanity validations; produces markdown report. |

---

## 🛠️ Data Engineering & Parsing Highlights

### 1. Robust Multilingual Extraction (`crawler/parse.py`)
- **JSON-LD Schema.org Support**: Extracts `Product.brand.name` (developer), `offers.price`, and structured `additionalProperty` entries.
- **Arabic-Indic Digit Normalization**: Translates Eastern Arabic numerals (`٠١٢٣٤٥٦٧٨٩` → `0123456789`) prior to regex parsing.
- **Unit & Million Multiplier Resolution**: Accurately parses values like `"1.5 مليون"` into `1,500,000` while stripping commas and currency symbols (`ج.م`).
- **Semantic Financial Block Parsing**: Reads HTML `<dl>` lists for remaining developer payments (`المتبقي للمطور`), installment amounts (`القسط`), and payment frequencies.
- **Amenity Tokenization**: Dual-channel extraction parsing checkmark-delineated bullet items (`✓`) and keyword matching across descriptions.

### 2. Standardization & Derivations (`etl/clean.py`)
- **Canonical Property Type Taxonomy**: Maps over 20 colloquial Arabic and English terms to the 8 schema types:
  - `"شقة"`, `"شقه"` $\rightarrow$ `apartment`
  - `"فيلا"`, `"فيلانا"` $\rightarrow$ `villa`
  - `"تاون هاوس"`, `"توين هاوس"`, `"تاونهاوس"` $\rightarrow$ `townhouse`
  - `"دوبلكس"`, `"دوبليكس"` $\rightarrow$ `duplex`
  - `"شاليه"`, `"شاليهة"` $\rightarrow$ `chalet`
  - `"بنتهاوس"`, `"بنت هاوس"` $\rightarrow$ `penthouse`
  - `"ستوديو"`, `"استوديو"` $\rightarrow$ `studio`
- **Geographic Normalization**: Unifies geographic variants into canonical Egyptian real estate hubs (e.g. `"New Cairo"` / `"التجمع الخامس"`, `"6 October"` / `"6 أكتوبر"`, `"New Capital"` / `"العاصمة الإدارية"`).

### 3. Realistic Synthetic User & Review Seeding (`etl/seed_users.py`)
- **Egyptian Demographics**: Generates culturally representative Egyptian names via `Faker("ar_EG")`.
- **Realistic Rating Distribution**: Reviews follow a realistic skewed satisfaction profile:
  - 1–3 stars: 10%
  - 4–5 stars: 15%
  - 6–7 stars: 30%
  - 8–9 stars: 35%
  - 10 stars: 10%
- **Constraint Compliance**: Guarantees all review authors exist in `User`, all reviewed developments exist in `Development`, and the composite unique constraint `(user_id, development_id)` is never violated.

---

## 📐 Formulas for Derived Metrics

1. **Total Asking Price (`asking_price`)**:
   - For **installment** properties:
     $$\text{Total Asking Price} = \text{Down Payment (المطلوب كاش دلوقتي)} + \text{Remaining to Developer (المتبقي للمطور)}$$
   - For **cash** properties:
     $$\text{Total Asking Price} = \text{Cash Price (المطلوب كاش)}$$
2. **Price per Square Meter (`price_per_sqm`)**:
   $$\text{Price per m}^2 = \frac{\text{Total Asking Price}}{\text{Total Area (m}^2\text{)}}$$
   *(Guarded: $\text{area} > 0$, verified against realistic Egyptian market boundaries $1,000 \le \text{EGP/m}^2 \le 5,000,000$).*
3. **Down Payment (`down_payment`)**:
   - Immediate cash equity required to purchase the listing or take over the contract:
     $$\text{Down Payment} = \text{Cash Required Now (المطلوب كاش دلوقتي)}$$
   - Validated constraint: $\text{Down Payment} \le \text{Total Asking Price}$.
4. **Gain over Market (`gain_over_market`)**:
   $$\text{Gain \%} = \frac{\text{Gain EGP}}{\text{Total Asking Price}} \times 100$$
5. **Discount over Market (`discount_over_market`)**:
   $$\text{Discount \%} = \frac{\text{Market Price} - \text{Total Asking Price}}{\text{Market Price}} \times 100$$

---

## 📊 Data Completeness & Verification Metrics

Auto-generated from [`validation/validate.py`](validation/validate.py) and documented in [`docs/milestone-2/validation_report.md`](docs/milestone-2/validation_report.md):

### 1. Crawl Completeness
- **Total Discovered in Sitemap:** 8,589
- **Crawled (Done):** 8,596 (100% complete)
- **Failed / Unreachable:** 1 (handled gracefully without terminating the crawler)
- **Pending URLs:** 0

### 2. Table Row Count Verification (DB vs CSV Parity)
| Table | DB Rows | CSV Rows | Status | Parity |
|---|---|---|---|:---:|
| `Location` | 197 | 197 | ✓ OK | 100% |
| `Developer` | 2,813 | 2,813 | ✓ OK | 100% |
| `Development` | 5,683 | 5,683 | ✓ OK | 100% |
| `Property` | 8,602 | 8,602 | ✓ OK | 100% |
| `Amenity` | 20 | 20 | ✓ OK | 100% |
| `Property_Amenity` | 62,998 | 62,998 | ✓ OK | 100% |
| `User` | 200 | 200 | ✓ OK | 100% |
| `User_Focus_Area` | 1,259 | 1,259 | ✓ OK | 100% |
| `Review` | 64,486 | 64,486 | ✓ OK | 100% |

### 3. Referential Integrity & Sanity Checks
- **Orphan Foreign Keys:** 0 across all parent-child relationships.
- **Duplicate Source URLs:** 0 duplicates detected.
- **Physical Bounds:** 0 properties with area $\le 0$, 0 properties with negative asking price.
- **Financial Bounds:** 0 properties where down payment exceeds asking price.
- **User Demographics:** 0 users with age $< 18$.
- **Review Ratings:** 0 reviews outside the valid range $[1, 10]$.

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- **Operating System:** Windows 10/11, macOS, or Linux
- **Python:** Python 3.11 or higher
- **Database:** MySQL Server 8.0+

### 2. Environment Setup
Clone the repository and install dependencies in a virtual environment:

```bash
# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
Create a `.env` file in the project root based on `.env.example`:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ResaleRealEstateDB
DB_USER=root
DB_PASS=your_password_here
```

Execute the Milestone I DDL schema script to initialize the database:
```bash
mysql -u root -p < ResaleRealEstateDB.sql
```

### 4. Running the Pipeline

#### Execute Full End-to-End Pipeline
```bash
python run_pipeline.py
```

#### Run with Page Limit (Quick Verification)
```bash
# Limit crawler fetch to 20 pages for rapid smoke testing
python run_pipeline.py --limit 20
```

#### Run or Resume Specific Stages
```bash
# Skip fetching and run parsing, cleaning, loading, seeding, export & validation
python run_pipeline.py --start-stage parse

# Run ONLY the CSV export stage
python run_pipeline.py --only-stage export

# Run ONLY the data integrity validator
python run_pipeline.py --only-stage validate
```

#### Run Individual Pipeline Modules Directly
```bash
# Stage 1: Sitemap discovery
python -m crawler.discover

# Stage 2: Crawl HTML pages
python -m crawler.fetch

# Stage 5: Load into MySQL
python -m etl.load

# Stage 6: Seed synthetic users and reviews
python -m etl.seed_users

# Stage 7: Export all tables to UTF-8-BOM CSV
python -m etl.export_csv

# Stage 8: Run data validation report
python -m validation.validate
```

---

## 🧪 Unit Testing

The repository includes a comprehensive unit test suite written in `pytest` verifying Arabic parsing, digit conversions, property type mappings, and financial derivations across diverse sample fixtures:

```bash
pytest tests/test_parse.py -v
```

**Test Coverage Summary:**
- Normalization of Arabic-Indic digits (`test_normalise_digits`).
- Fallback property type classification (`test_normalise_type`).
- Extraction of monetary figures, discounts, and millions (`test_parse_num`).
- Verification that pure-function parsers handle missing tags gracefully without runtime exceptions.
- **Result:** **112 passing tests, 0 failures.**

---

## 🔍 Milestone III Preparedness & Analytical Smoke Tests

All 8 complex analytical queries specified for the upcoming Milestone III application layer are implemented and smoke-tested in [`validation/milestone3_smoke_tests.sql`](validation/milestone3_smoke_tests.sql):

1. **User Reviews Exploration**: Register user, record review, and inspect all reviews for top developments ordered by date.
2. **Top Projects by Inventory & Gain**: Group by property type to find projects with highest listing volume, total resale amount, and average market gain.
3. **Compound Details & Pricing**: Retrieve development locations, average price/sqm, and listing counts per unit type.
4. **Area Price Bands**: Analyze price distribution, minimum, maximum, and average price/sqm for any given region (e.g., North Coast / `الساحل الشمالي`).
5. **Multi-Amenity Search**: Filter properties in specific areas within price bounds possessing multiple conjunct amenities (e.g., Swimming Pool **AND** Gym).
6. **Developer Performance Ranking**: Rank top 5 real estate developers by listing volume, average price/sqm, and average down payment.
7. **Temporal Resale Trends**: Group listings by area, property type, and original contract year.
8. **Financial Maturity & Discount Analysis**: Calculate average installment price, down payment, discount percentage, contract age, and market price per project.

To execute the smoke test suite:
```bash
mysql -u root -p ResaleRealEstateDB < validation/milestone3_smoke_tests.sql
```

---

## 💾 Database Dump & Restore Verification

### Generating the MySQL Dump
The full database dump is exported with full transaction isolation and UTF-8 collation:
```bash
mysqldump --single-transaction --routines --default-character-set=utf8mb4 -u root -p ResaleRealEstateDB --result-file=output/resale_db_dump.sql
```

### Clean Restore Verification
To verify the reproducibility of the dump file:
```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS test_restore_db; CREATE DATABASE test_restore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p --default-character-set=utf8mb4 test_restore_db < output/resale_db_dump.sql
mysql -u root -p -e "SHOW TABLES FROM test_restore_db; SELECT COUNT(*) FROM test_restore_db.Property;"
```
*(Verified: all 9 tables restore with 100% record parity and intact foreign keys).*

---

## 📂 Detailed Repository Layout

```text
csce2501-project-database/
├── README.md                           # Master project guide & deliverables index
├── ResaleRealEstateDB.sql              # Milestone I MySQL DDL schema script (9 tables)
├── config.py                           # Central configuration (crawler, db, paths)
├── requirements.txt                    # Python runtime dependencies
├── run_pipeline.py                     # Master CLI pipeline runner (stages 1-8)
├── crawl_state.sqlite                  # SQLite persistent crawler state store
├── crawl.log                           # Full crawler activity and event log
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
│       ├── Amenity.csv
│       ├── Developer.csv
│       ├── Development.csv
│       ├── Location.csv
│       ├── Property.csv
│       ├── Property_Amenity.csv
│       ├── Review.csv
│       ├── User.csv
│       └── User_Focus_Area.csv
│
├── samples/                            # Offline test fixtures & cached samples
│   ├── detail_*.html                   # Diverse property detail sample HTML pages
│   ├── property_urls.txt               # Enumerate listing URLs from sitemap (8,589)
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

## 👥 Course & Academic Information

- **Course:** CSCE 2501: Fundamentals of Database Systems
- **Institution:** The American University in Cairo (AUC)
- **Term:** Fall 2026
- **Database Engine:** MySQL Server 8.0 (InnoDB engine, `utf8mb4_unicode_ci` collation)