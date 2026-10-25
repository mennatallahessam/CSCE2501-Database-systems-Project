# AqarExit Reconnaissance Report (Phase 0)

## 1. Overview & Source Architecture

- **Target Site:** [AqarExit](https://aqarexit.com/en/opportunities) — an Egyptian resale real-estate platform specializing in secondary market contracts and off-plan resales.
- **Data Delivery Method:** Server-Side Rendered (SSR) HTML pages with embedded `application/ld+json` (Schema.org `Product`) structured metadata and microdata in definition lists (`<dl>`, `<dt>`, `<dd>`).
- **Inspection Findings:**
  - `robots.txt` disallows administrative/auth paths (`/admin`, `/api/internal`) but permits property discovery via `https://aqarexit.com/sitemap.xml`.
  - The sitemap directly enumerates **8,110 property URLs** matching pattern: `https://aqarexit.com/buy/opportunity/<uuid>` (and its localized variant `.../en/buy/...`).
  - No client-side headless rendering (Selenium/Playwright) is required; plain HTTP requests using `requests` with standard browser headers and session pooling reliably retrieve the complete document.

## 2. Extraction Strategy

We choose **HTML + Embedded Schema.org JSON parsing** (`BeautifulSoup` + `json` + `re`):
1. **Primary Structured Source (`application/ld+json`):**
   - Brand name → `Developer.developer_name`
   - Description → `Property.description`
   - Offers price → `Property.asking_price` (resale cash component)
   - Additional properties: unit type, delivery year, delivery status.
2. **Microdata & Detail Elements (`<dl>`, `<dt>`, `<dd>` & badge text):**
   - "المتبقي للمطور" → remaining installment balance owed to developer
   - "المطلوب كاش" → down payment required immediately to acquire resale contract
   - "القسط" → recurring installment amount and frequency
   - "سنة التعاقد" → contract year
   - "التشطيب" → finishing specification
   - "غرف" / "حمامات" → bedroom and bathroom counts
   - Checkmark amenity lists → `Amenity` and `Property_Amenity`
3. **Derived Metrics:**
   - Total Asking Price = Cash down payment + remaining installments to developer
   - Price per m² = Total Asking Price / Total Area m²
   - Gain / Discount over market = calculated against prevailing market price when published

## 3. Site Field to Schema Mapping

| Site Field / Selector | Schema Table | Schema Column | Extraction Method / Logic |
| :--- | :--- | :--- | :--- |
| `<h1>` header text | `Development` | `project_name` | Direct text extraction |
| `ld+json` Product `brand.name` | `Developer` | `developer_name` | JSON lookup, fallback to text regex |
| Breadcrumbs / area badges | `Location` | `city`, `area_name`, `compound_name` | Canonical mapping & normalized Arabic text |
| Canonical listing URL | `Property` | `source_url` | Natural key deduplication |
| `ld+json` Product `name` | `Property` | `title` | Truncated to 255 characters |
| `ld+json` Product `description` | `Property` | `description` | Full text preserved for audit |
| "المساحة" badge / spec text | `Property` | `total_area_sqm` | Numeric extraction with digit normalization |
| "غرف" badge | `Property` | `num_bedrooms` | Integer parse (0–20 range guard) |
| "حمامات" badge | `Property` | `num_bathrooms` | Integer parse (0–20 range guard) |
| "النوع" / `ld+json` category | `Property` | `property_type` | Mapped to controlled vocabulary: `apartment`, `villa`, `townhouse`, `duplex`, `chalet`, `penthouse`, `studio`, `other` |
| "المطلوب كاش" + "المتبقي للمطور" | `Property` | `asking_price` | Total cost to own the unit |
| Derived | `Property` | `price_per_sqm` | `asking_price / total_area_sqm` |
| "المطلوب كاش" | `Property` | `down_payment` | Cash amount required at resale purchase |
| "طريقة الدفع" / installment checks | `Property` | `payment_method` | `cash` or `installment` |
| "سنة التعاقد" | `Property` | `contract_year` | 4-digit year regex (1980–2030 guard) |
| "مكسبك عن سعر السوق" | `Property` | `gain_over_market` | Percentage gain over market |
| Derived from market vs asking | `Property` | `discount_over_market` | Percentage discount |
| Feature checkmarks / text | `Amenity` | `amenity_name` | Canonical English lookup (`Swimming Pool`, `Gym`, `Security`, etc.) |

## 4. Fields Not Provided by Site & Handling

- **User Accounts & Focus Areas:** AqarExit is a listing aggregator and does not expose buyer profiles or registration records. Handled via synthetic generator (`etl/seed_users.py`) with reproducible seed (`SEED_RANDOM_SEED=42`), producing consistent age/birthdate, Egyptian email patterns, and focus areas linked to actual crawled locations.
- **Reviews:** Listing pages do not have a public user review section. Handled via synthetic review generator (`Review` table) referencing existing `Development` rows with realistic sentiment distribution (ratings 1–10).
- **Gain / Discount Over Market:** Only available on listings that provide an explicit appraisal comparison. If absent, set cleanly to `NULL` (never fabricated).
