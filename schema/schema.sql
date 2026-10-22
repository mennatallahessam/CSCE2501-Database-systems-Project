-- ============================================================
-- CSCE 2501: Fundamentals of Database Systems
-- Milestone I: Database Design & Implementation
-- Resale Real Estate Database — MySQL Script
-- ============================================================

-- Safely drop and recreate the database
DROP DATABASE IF EXISTS ResaleRealEstateDB;
CREATE DATABASE ResaleRealEstateDB;
USE ResaleRealEstateDB;

-- ============================================================
-- INDEPENDENT TABLES (No Foreign Keys)
-- ============================================================

-- ----------------------------------------------------------
-- 1. Location Table
-- Stores hierarchical location data for properties and
-- developments (city, district, area, compound).
-- ----------------------------------------------------------
CREATE TABLE Location (
    location_id         INT             AUTO_INCREMENT,
    city                VARCHAR(100)    NOT NULL,
    district            VARCHAR(100),
    area_name           VARCHAR(100),
    compound_name       VARCHAR(150),

    PRIMARY KEY (location_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 2. Developer Table
-- Stores real estate developer corporate information
-- and tracking metrics.
-- ----------------------------------------------------------
CREATE TABLE Developer (
    developer_id            INT             AUTO_INCREMENT,
    developer_name          VARCHAR(150)    NOT NULL,
    corporate_details       TEXT,
    total_projects          INT             DEFAULT 0,
    total_properties_listed INT             DEFAULT 0,

    PRIMARY KEY (developer_id),
    UNIQUE (developer_name)
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 3. User Table
-- Stores registered user information including
-- demographics and authentication details.
-- ----------------------------------------------------------
CREATE TABLE `User` (
    user_id         INT             AUTO_INCREMENT,
    username        VARCHAR(50)     NOT NULL,
    email           VARCHAR(100)    NOT NULL,
    password_hash   VARCHAR(255)    NOT NULL,
    gender          VARCHAR(10),
    age             INT,
    birthdate       DATE,

    PRIMARY KEY (user_id),
    UNIQUE (username),
    UNIQUE (email),
    CHECK (gender IN ('Male', 'Female')),
    CHECK (age >= 18)
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 4. Amenity Table
-- Lookup table storing distinct amenity types
-- (e.g., pool, gym, parking, garden, security).
-- ----------------------------------------------------------
CREATE TABLE Amenity (
    amenity_id      INT             AUTO_INCREMENT,
    amenity_name    VARCHAR(100)    NOT NULL,

    PRIMARY KEY (amenity_id),
    UNIQUE (amenity_name)
) ENGINE=InnoDB;

-- ============================================================
-- DEPENDENT TABLES (Have Foreign Keys)
-- ============================================================

-- ----------------------------------------------------------
-- 5. Development Table
-- Represents real estate development projects, each
-- belonging to one developer and located in one location.
-- ----------------------------------------------------------
CREATE TABLE Development (
    development_id  INT             AUTO_INCREMENT,
    project_name    VARCHAR(200)    NOT NULL,
    description     TEXT,
    developer_id    INT             NOT NULL,
    location_id     INT             NOT NULL,

    PRIMARY KEY (development_id),

    FOREIGN KEY (developer_id)
        REFERENCES Developer(developer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (location_id)
        REFERENCES Location(location_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 6. Property Table
-- Core table storing all property listing details:
-- physical specs, financial info, contract details.
-- Each property belongs to a development and a location.
-- ----------------------------------------------------------
CREATE TABLE Property (
    property_id         INT             AUTO_INCREMENT,
    title               VARCHAR(255)    NOT NULL,
    description         TEXT,
    source_url          VARCHAR(500),
    total_area_sqm      DECIMAL(10,2),
    num_bedrooms        INT,
    num_bathrooms       INT,
    property_type       VARCHAR(50),
    asking_price        DECIMAL(12,2),
    price_per_sqm       DECIMAL(10,2),
    payment_method      VARCHAR(20),
    down_payment        DECIMAL(12,2),
    contract_year       INT,
    discount_over_market DECIMAL(5,2),
    gain_over_market    DECIMAL(5,2),
    development_id      INT,
    location_id         INT,

    PRIMARY KEY (property_id),

    FOREIGN KEY (development_id)
        REFERENCES Development(development_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (location_id)
        REFERENCES Location(location_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CHECK (property_type IN (
        'apartment', 'villa', 'townhouse', 'duplex',
        'chalet', 'penthouse', 'studio', 'other'
    )),

    CHECK (payment_method IN ('cash', 'installment')),

    CHECK (num_bedrooms >= 0),
    CHECK (num_bathrooms >= 0),
    CHECK (total_area_sqm > 0),
    CHECK (asking_price >= 0)
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 7. Property_Amenity Table (Junction / Associative)
-- Resolves the M:N relationship between Property and
-- Amenity. A property can have many amenities, and an
-- amenity can belong to many properties.
-- ----------------------------------------------------------
CREATE TABLE Property_Amenity (
    property_id     INT     NOT NULL,
    amenity_id      INT     NOT NULL,

    PRIMARY KEY (property_id, amenity_id),

    FOREIGN KEY (property_id)
        REFERENCES Property(property_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (amenity_id)
        REFERENCES Amenity(amenity_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 8. User_Focus_Area Table (Junction / Associative)
-- Resolves the M:N relationship between User and Location.
-- Users can specify multiple areas of focus/interest.
-- ----------------------------------------------------------
CREATE TABLE User_Focus_Area (
    user_id         INT     NOT NULL,
    location_id     INT     NOT NULL,

    PRIMARY KEY (user_id, location_id),

    FOREIGN KEY (user_id)
        REFERENCES `User`(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (location_id)
        REFERENCES Location(location_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 9. Review Table
-- Stores user reviews for development projects.
-- Each user can submit at most one review per development.
-- Rating must be between 1 and 10.
-- ----------------------------------------------------------
CREATE TABLE Review (
    review_id       INT             AUTO_INCREMENT,
    user_id         INT             NOT NULL,
    development_id  INT             NOT NULL,
    rating          INT             NOT NULL,
    review_comment  TEXT,
    review_date     DATE            NOT NULL,

    PRIMARY KEY (review_id),

    FOREIGN KEY (user_id)
        REFERENCES `User`(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (development_id)
        REFERENCES Development(development_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CHECK (rating BETWEEN 1 AND 10),

    UNIQUE (user_id, development_id)
) ENGINE=InnoDB;

-- ============================================================
-- END OF SCHEMA SCRIPT
-- ============================================================
-- Summary of Tables Created:
-- 1. Location           (Independent)
-- 2. Developer           (Independent)
-- 3. User                (Independent)
-- 4. Amenity             (Independent)
-- 5. Development         (FK → Developer, Location)
-- 6. Property            (FK → Development, Location)
-- 7. Property_Amenity    (FK → Property, Amenity)        [Junction]
-- 8. User_Focus_Area     (FK → User, Location)           [Junction]
-- 9. Review              (FK → User, Development)
-- ============================================================
