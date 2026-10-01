# Relational Model (Schema Mapping)
## Resale Real Estate Database — CSCE 2501 Milestone I

---

> **Notation:**  
> - **Underlined** attributes denote **Primary Keys (PK)**.  
> - *Italicized* attributes denote **Foreign Keys (FK)**.  
> - All schemas are normalized to at least **3NF / BCNF**.

---

## Relational Schemas

### 1. Location
```
Location(__location_id__, city, district, area_name, compound_name)
```
- PK: `location_id`
- No foreign keys (independent entity).

---

### 2. Developer
```
Developer(__developer_id__, developer_name, corporate_details, total_projects, total_properties_listed)
```
- PK: `developer_id`
- UNIQUE: `developer_name`
- No foreign keys (independent entity).

---

### 3. Development
```
Development(__development_id__, project_name, description, *developer_id*, *location_id*)
```
- PK: `development_id`
- FK: `developer_id` → `Developer(developer_id)` ON DELETE RESTRICT ON UPDATE CASCADE
- FK: `location_id` → `Location(location_id)` ON DELETE RESTRICT ON UPDATE CASCADE

---

### 4. Property
```
Property(__property_id__, title, description, source_url, total_area_sqm, num_bedrooms, num_bathrooms, property_type, asking_price, price_per_sqm, payment_method, down_payment, contract_year, discount_over_market, gain_over_market, *development_id*, *location_id*)
```
- PK: `property_id`
- FK: `development_id` → `Development(development_id)` ON DELETE CASCADE ON UPDATE CASCADE
- FK: `location_id` → `Location(location_id)` ON DELETE RESTRICT ON UPDATE CASCADE
- CHECK: `property_type` IN ('apartment', 'villa', 'townhouse', 'duplex', 'chalet', 'penthouse', 'studio', 'other')
- CHECK: `payment_method` IN ('cash', 'installment')

---

### 5. Amenity
```
Amenity(__amenity_id__, amenity_name)
```
- PK: `amenity_id`
- UNIQUE: `amenity_name`
- No foreign keys (independent/lookup entity).

---

### 6. Property_Amenity (Junction — resolves M:N between Property and Amenity)
```
Property_Amenity(__*property_id*__, __*amenity_id*__)
```
- COMPOSITE PK: (`property_id`, `amenity_id`)
- FK: `property_id` → `Property(property_id)` ON DELETE CASCADE ON UPDATE CASCADE
- FK: `amenity_id` → `Amenity(amenity_id)` ON DELETE CASCADE ON UPDATE CASCADE

---

### 7. User
```
User(__user_id__, username, email, password_hash, gender, age, birthdate)
```
- PK: `user_id`
- UNIQUE: `username`, `email`
- CHECK: `gender` IN ('Male', 'Female')
- CHECK: `age` >= 18

---

### 8. User_Focus_Area (Junction — resolves M:N between User and Location)
```
User_Focus_Area(__*user_id*__, __*location_id*__)
```
- COMPOSITE PK: (`user_id`, `location_id`)
- FK: `user_id` → `User(user_id)` ON DELETE CASCADE ON UPDATE CASCADE
- FK: `location_id` → `Location(location_id)` ON DELETE CASCADE ON UPDATE CASCADE

---

### 9. Review
```
Review(__review_id__, *user_id*, *development_id*, rating, review_comment, review_date)
```
- PK: `review_id`
- FK: `user_id` → `User(user_id)` ON DELETE CASCADE ON UPDATE CASCADE
- FK: `development_id` → `Development(development_id)` ON DELETE CASCADE ON UPDATE CASCADE
- CHECK: `rating` BETWEEN 1 AND 10
- UNIQUE: (`user_id`, `development_id`) — one review per user per development

---

## Normalization Verification

| Normal Form | Status | Justification |
|---|---|---|
| **1NF** | ✅ Satisfied | All attributes are atomic. Multi-valued attributes (amenities, focus areas) are resolved via junction tables. |
| **2NF** | ✅ Satisfied | No partial dependencies exist. All non-key attributes depend on the entire primary key in every relation. |
| **3NF** | ✅ Satisfied | No transitive dependencies exist. Every non-key attribute depends directly on the primary key. |
| **BCNF** | ✅ Satisfied | Every determinant is a candidate key in all relations. |

---

## Dependency Diagram (Table Creation Order)

```
Independent Tables (no FKs):
  1. Location
  2. Developer
  3. User
  4. Amenity

Dependent Tables (have FKs):
  5. Development    → depends on Developer, Location
  6. Property       → depends on Development, Location
  7. Property_Amenity → depends on Property, Amenity
  8. User_Focus_Area  → depends on User, Location
  9. Review          → depends on User, Development
```
