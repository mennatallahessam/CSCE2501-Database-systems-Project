-- ============================================================
-- validation/milestone3_smoke_tests.sql
-- Smoke-test queries for all 8 Milestone III requirements.
-- Run these after the full pipeline to verify data completeness.
-- ============================================================

USE ResaleRealEstateDB;

-- ─────────────────────────────────────────────────────────────
-- Q1: Register a user; add a review; view reviews of a project
-- ─────────────────────────────────────────────────────────────
-- View reviews for the top development by review count
SELECT
    d.project_name,
    u.username,
    r.rating,
    r.review_comment,
    r.review_date
FROM Review r
JOIN `User` u        ON r.user_id       = u.user_id
JOIN Development d   ON r.development_id = d.development_id
WHERE d.development_id = (
    SELECT development_id
    FROM Review
    GROUP BY development_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
ORDER BY r.review_date DESC
LIMIT 20;

-- ─────────────────────────────────────────────────────────────
-- Q2: Top 10 projects by resale inventory, resale amount,
--     and highest gain over market value — by property type
-- ─────────────────────────────────────────────────────────────
SELECT
    p.property_type,
    d.project_name,
    COUNT(p.property_id)           AS resale_count,
    SUM(p.asking_price)            AS total_resale_amount,
    AVG(p.gain_over_market)        AS avg_gain_pct
FROM Property p
JOIN Development d ON p.development_id = d.development_id
GROUP BY p.property_type, d.project_name
ORDER BY p.property_type, resale_count DESC
LIMIT 30;

-- ─────────────────────────────────────────────────────────────
-- Q3: Location of a development, avg price/sqm and count
--     of listings per unit type
-- ─────────────────────────────────────────────────────────────
SELECT
    d.project_name,
    l.city,
    l.area_name,
    p.property_type,
    COUNT(p.property_id)            AS num_listings,
    ROUND(AVG(p.price_per_sqm), 0) AS avg_price_per_sqm
FROM Property p
JOIN Development d ON p.development_id = d.development_id
JOIN Location l    ON p.location_id    = l.location_id
WHERE d.project_name IS NOT NULL
GROUP BY d.project_name, l.city, l.area_name, p.property_type
ORDER BY d.project_name, p.property_type;

-- ─────────────────────────────────────────────────────────────
-- Q4: All properties in an area, avg price/sqm per unit type
-- ─────────────────────────────────────────────────────────────
-- Change 'الساحل الشمالي' to any area of interest
SELECT
    l.area_name,
    p.property_type,
    COUNT(p.property_id)            AS count,
    ROUND(AVG(p.price_per_sqm), 0) AS avg_price_per_sqm,
    MIN(p.asking_price)             AS min_price,
    MAX(p.asking_price)             AS max_price
FROM Property p
JOIN Location l ON p.location_id = l.location_id
WHERE l.area_name = 'الساحل الشمالي'
GROUP BY l.area_name, p.property_type
ORDER BY p.property_type;

-- ─────────────────────────────────────────────────────────────
-- Q5: Properties in an area within a price range
--     having a given set of amenities
-- ─────────────────────────────────────────────────────────────
SELECT
    p.property_id,
    p.title,
    p.asking_price,
    p.total_area_sqm,
    p.price_per_sqm,
    l.area_name
FROM Property p
JOIN Location l ON p.location_id = l.location_id
WHERE l.area_name = 'التجمع الخامس'
  AND p.asking_price BETWEEN 2000000 AND 10000000
  AND p.property_id IN (
      SELECT pa.property_id
      FROM Property_Amenity pa
      JOIN Amenity a ON pa.amenity_id = a.amenity_id
      WHERE a.amenity_name = 'Swimming Pool'
  )
  AND p.property_id IN (
      SELECT pa.property_id
      FROM Property_Amenity pa
      JOIN Amenity a ON pa.amenity_id = a.amenity_id
      WHERE a.amenity_name = 'Gym'
  )
ORDER BY p.asking_price;

-- ─────────────────────────────────────────────────────────────
-- Q6: Top 5 developers by resale listings, avg price/sqm,
--     avg down payment, avg gain over market value
-- ─────────────────────────────────────────────────────────────
SELECT
    dev.developer_name,
    COUNT(p.property_id)            AS resale_listings,
    ROUND(AVG(p.price_per_sqm), 0) AS avg_price_per_sqm,
    ROUND(AVG(p.down_payment), 0)  AS avg_down_payment,
    ROUND(AVG(p.gain_over_market), 2) AS avg_gain_pct
FROM Property p
JOIN Development d  ON p.development_id = d.development_id
JOIN Developer dev  ON d.developer_id   = dev.developer_id
GROUP BY dev.developer_name
ORDER BY resale_listings DESC
LIMIT 5;

-- ─────────────────────────────────────────────────────────────
-- Q7: Properties by area, property type and contract year
-- ─────────────────────────────────────────────────────────────
SELECT
    l.area_name,
    p.property_type,
    p.contract_year,
    COUNT(p.property_id)  AS count,
    AVG(p.asking_price)   AS avg_price
FROM Property p
JOIN Location l ON p.location_id = l.location_id
WHERE p.contract_year IS NOT NULL
GROUP BY l.area_name, p.property_type, p.contract_year
ORDER BY l.area_name, p.property_type, p.contract_year;

-- ─────────────────────────────────────────────────────────────
-- Q8: Average installment price, avg down payment,
--     count, avg discount, avg contract year age,
--     avg market price — by area and development
-- ─────────────────────────────────────────────────────────────
SELECT
    l.area_name,
    d.project_name,
    COUNT(p.property_id)                         AS num_properties,
    ROUND(AVG(p.down_payment), 0)               AS avg_down_payment,
    ROUND(AVG(p.discount_over_market), 2)       AS avg_discount_pct,
    ROUND(AVG(YEAR(CURDATE()) - p.contract_year), 1) AS avg_contract_age_years,
    ROUND(AVG(p.asking_price), 0)               AS avg_asking_price
FROM Property p
JOIN Development d ON p.development_id = d.development_id
JOIN Location l    ON p.location_id    = l.location_id
WHERE p.contract_year IS NOT NULL
GROUP BY l.area_name, d.project_name
ORDER BY l.area_name, num_properties DESC;
