# CSCE 2501: Fundamentals of Database Systems — Project
## Resale Real Estate Database (Egypt Secondary Market)

A production-grade relational database and end-to-end data acquisition pipeline for Egypt's resale real-estate properties, based on [AqarExit](https://aqarexit.com/en/opportunities).

---

## 📦 Milestone II: Web Crawler, ETL & Database Population

### Deliverables Checklist

| # | Deliverable | Location / Command |
|---|---|---|
| 1 | **Reconnaissance Report** | [`RECON.md`](RECON.md) |
| 2 | **Web Crawler & Pipeline** | [`run_pipeline.py`](run_pipeline.py), [`crawler/`](crawler/), [`etl/`](etl/) |
| 3 | **Unit Test Suite** | [`tests/test_parse.py`](tests/test_parse.py) (112 test cases) |
| 4 | **MySQL Database Dump** | [`output/resale_db_dump.sql`](output/resale_db_dump.sql) |
| 5 | **UTF-8 with BOM CSVs** | [`output/csv/`](output/csv/) (all 9 tables) |
| 6 | **Validation Report** | [`validation_report.md`](validation_report.md) |
| 7 | **Milestone III Smoke Tests**| [`validation/milestone3_smoke_tests.sql`](validation/milestone3_smoke_tests.sql) |

---

## 🏗️ Architecture & Pipeline Flow

```
[ AqarExit Sitemap ]
        │
        ▼ (Stage 1: discover)
[ samples/property_urls.txt (8,110 URLs) ]
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
  [ validation_report.md & milestone3_smoke_tests.sql ]
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

- Post-load validation report is generated at [`validation_report.md`](validation_report.md).
- All 8 analytical queries required for Milestone III application layer are verified in [`validation/milestone3_smoke_tests.sql`](validation/milestone3_smoke_tests.sql).

---

## 👥 Course & Term

CSCE 2501: Fundamentals of Database Systems — AUC, Fall 2026