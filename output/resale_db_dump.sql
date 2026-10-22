-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: resalerealestatedb
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `amenity`
--

DROP TABLE IF EXISTS `amenity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenity` (
  `amenity_id` int NOT NULL AUTO_INCREMENT,
  `amenity_name` varchar(100) NOT NULL,
  PRIMARY KEY (`amenity_id`),
  UNIQUE KEY `amenity_name` (`amenity_name`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenity`
--

LOCK TABLES `amenity` WRITE;
/*!40000 ALTER TABLE `amenity` DISABLE KEYS */;
INSERT INTO `amenity` VALUES (14,'Club House'),(2,'Elevator'),(3,'Garden'),(5,'Lagoon'),(15,'Parking'),(1,'Roof'),(6,'Sea View'),(18,'Security'),(28,'Swimming Pool'),(13,'أمن 24 ساعة'),(38,'جاردن خاصة'),(17,'قريبة من الخدمات'),(4,'مول');
/*!40000 ALTER TABLE `amenity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `developer`
--

DROP TABLE IF EXISTS `developer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `developer` (
  `developer_id` int NOT NULL AUTO_INCREMENT,
  `developer_name` varchar(150) NOT NULL,
  `corporate_details` text,
  `total_projects` int DEFAULT '0',
  `total_properties_listed` int DEFAULT '0',
  PRIMARY KEY (`developer_id`),
  UNIQUE KEY `developer_name` (`developer_name`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `developer`
--

LOCK TABLES `developer` WRITE;
/*!40000 ALTER TABLE `developer` DISABLE KEYS */;
INSERT INTO `developer` VALUES (1,'Tabrouk developments sodic',NULL,0,0),(3,'ماونتن فيو',NULL,0,0),(4,'Orascom Developments',NULL,0,0),(5,'هايد بارك سي شور',NULL,0,0),(6,'طلعت مصطفى',NULL,0,0),(13,'كونكريت',NULL,0,0),(14,'Tatweer misr',NULL,0,0),(15,'Hyde park',NULL,0,0);
/*!40000 ALTER TABLE `developer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `development`
--

DROP TABLE IF EXISTS `development`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `development` (
  `development_id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(200) NOT NULL,
  `description` text,
  `developer_id` int NOT NULL,
  `location_id` int NOT NULL,
  PRIMARY KEY (`development_id`),
  KEY `developer_id` (`developer_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `development_ibfk_1` FOREIGN KEY (`developer_id`) REFERENCES `developer` (`developer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `development_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `development`
--

LOCK TABLES `development` WRITE;
/*!40000 ALTER TABLE `development` DISABLE KEYS */;
INSERT INTO `development` VALUES (1,'June by sodic',NULL,1,1),(2,'اي سيتي اكتوبر',NULL,3,2),(3,'OWest',NULL,4,2),(4,'هايد بارك سي شور لاجون تاون',NULL,5,1),(5,'Southmed',NULL,6,1),(6,'چوار',NULL,13,3),(7,'Salt',NULL,14,4),(8,'Seashore',NULL,15,4);
/*!40000 ALTER TABLE `development` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(100) NOT NULL,
  `district` varchar(100) DEFAULT NULL,
  `area_name` varchar(100) DEFAULT NULL,
  `compound_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (1,'الساحل الشمالي',NULL,'الساحل الشمالي',NULL),(2,'6 أكتوبر',NULL,'6 أكتوبر',NULL),(3,'التجمع الخامس',NULL,'التجمع الخامس',NULL),(4,'رأس الحكمة',NULL,'رأس الحكمة',NULL);
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property` (
  `property_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `source_url` varchar(500) DEFAULT NULL,
  `total_area_sqm` decimal(10,2) DEFAULT NULL,
  `num_bedrooms` int DEFAULT NULL,
  `num_bathrooms` int DEFAULT NULL,
  `property_type` varchar(50) DEFAULT NULL,
  `asking_price` decimal(12,2) DEFAULT NULL,
  `price_per_sqm` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `down_payment` decimal(12,2) DEFAULT NULL,
  `contract_year` int DEFAULT NULL,
  `discount_over_market` decimal(5,2) DEFAULT NULL,
  `gain_over_market` decimal(5,2) DEFAULT NULL,
  `development_id` int DEFAULT NULL,
  `location_id` int DEFAULT NULL,
  PRIMARY KEY (`property_id`),
  KEY `development_id` (`development_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `property_ibfk_1` FOREIGN KEY (`development_id`) REFERENCES `development` (`development_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `property_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `property_chk_1` CHECK ((`property_type` in (_utf8mb4'apartment',_utf8mb4'villa',_utf8mb4'townhouse',_utf8mb4'duplex',_utf8mb4'chalet',_utf8mb4'penthouse',_utf8mb4'studio',_utf8mb4'other'))),
  CONSTRAINT `property_chk_2` CHECK ((`payment_method` in (_utf8mb4'cash',_utf8mb4'installment'))),
  CONSTRAINT `property_chk_3` CHECK ((`num_bedrooms` >= 0)),
  CONSTRAINT `property_chk_4` CHECK ((`num_bathrooms` >= 0)),
  CONSTRAINT `property_chk_5` CHECK ((`total_area_sqm` > 0)),
  CONSTRAINT `property_chk_6` CHECK ((`asking_price` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property`
--

LOCK TABLES `property` WRITE;
/*!40000 ALTER TABLE `property` DISABLE KEYS */;
INSERT INTO `property` VALUES (1,'June by sodic — بنتهاوس 155 م² · 3 غرف · الساحل الشمالي · كاش 8.5 مليون ج.م','بينت هاوس في مشروع چون اكوا بينت هاوس لاجون ڤيو وليها اسانسير منفصل عن بقيت اليونت','https://aqarexit.com/buy/opportunity/detail_1',155.00,3,3,'penthouse',16149000.00,104187.10,'installment',8500000.00,2023,NULL,NULL,1,1),(2,'June by sodic — بنتهاوس 155 م² · 3 غرف · الساحل الشمالي · كاش 8.5 مليون ج.م','بينت هاوس في مشروع چون اكوا بينت هاوس لاجون ڤيو وليها اسانسير منفصل عن بقيت اليونت','https://aqarexit.com/buy/opportunity/detail_1_efc811dc',155.00,3,3,'penthouse',16149000.00,104187.10,'installment',8500000.00,2023,NULL,NULL,1,1),(3,'اي سيتي اكتوبر — شقة 175 م² · 3 غرف · 6 أكتوبر · كاش 3.8 مليون ج.م','موقع مميز جداا','https://aqarexit.com/buy/opportunity/detail_2_04a168da',175.00,3,3,'apartment',9897499.00,56557.14,'installment',3773420.00,2024,NULL,NULL,2,2),(4,'OWest — دوبلكس 212 م² · 3 غرف · 6 أكتوبر · كاش 3.5 مليون ج.م','دوبلكس نصف تشطيب ٢١٢ متر مربع مكون من طابقين بكومباوند او ويست مكونه من ٣ غرف و ٣ حمامات و عدد من البلكونات - طابق ٤ و ٥ مطله على منطقة البرك و غير مجروحه','https://aqarexit.com/buy/opportunity/detail_3_9bc6bb46',212.00,3,3,'duplex',17426000.00,82198.11,'installment',3485252.00,2024,NULL,NULL,3,2),(5,'هايد بارك سي شور لاجون تاون — شاليه 80 م² · 1 غرف · الساحل الشمالي · كاش 3.3 مليون ج.م','شاليه هايد بارك سي شور لاجون تاون ٨٠ متر مربعة غرفة تتقسم غرفتين بحري علي فيو كريستال لاجون مفتوح ٣٨ متر فيو تعتبر مبنية الاستلام سنة ونص انا شاريها من سنتين ونص ببيعها للتعارف مش عارف أسدد ما فيشزيها بيتباع في الشركة فيه مرحلة غير مميزة في ءاخر المشروع المفروض ءاخر حاجة وكدة الشركة ما فيهاش متاح ونفس المساحة من ١١ الى ١١.٥٠٠ مليون ولسه الاستلام متأخر،المشروع الشاطيء شغال والفندق ممكن تروح الشاطيء الان،الوحدة اخترتها مميزة ،وجزيتم خيرا','https://aqarexit.com/buy/opportunity/detail_4_1ba2e3e8',80.00,1,1,'chalet',9240000.00,115500.00,'installment',3275580.00,2024,NULL,NULL,4,1),(6,'Southmed — شاليه 142 م² · 3 غرف · الساحل الشمالي · كاش 4.5 مليون ج.م','شاليه مميز جدا ارضي بجاردن اول يوم حجز، تميز L10 شايف المرينا والبحر مباشر الاستلام 7/2028 السعر شامل وديعه الصيانه','https://aqarexit.com/buy/opportunity/detail_5_0f889c3e',142.00,3,3,'chalet',19215000.00,135316.90,'installment',4500000.00,2024,NULL,NULL,5,1),(7,'چوار — شقة 101 م² · 2 غرف · التجمع الخامس · كاش 666 ألف ج.م','كومبوند چوار التجمع السادس 101 متر بجوار هايد بارك و زد اورا التجمع السادس','https://aqarexit.com/buy/opportunity/2cd1b47b-4f06-4815-8a2f-ee39a634ff31',101.00,2,2,'apartment',3928000.00,38891.09,'installment',666000.00,2025,NULL,NULL,6,3),(8,'Salt — تاون هاوس 150 م² · 3 غرف · رأس الحكمة · كاش 3.8 مليون ج.م','تاون هاوس بمشروع سولت راس الحكمه وحده مشطبه بالكامل تشطيبات عاليه الجوده','https://aqarexit.com/buy/opportunity/3a6e0d7d-50b9-4142-b2fb-fb70c24ea04b',150.00,3,3,'townhouse',19151000.00,127673.33,'installment',3830000.00,2025,NULL,NULL,7,4),(9,'Seashore — شاليه 86 م² · 2 غرف · رأس الحكمة · كاش 2.3 مليون ج.م','شاليه ارضي بجاردن ٤٠ م غرفتين و حمامين','https://aqarexit.com/buy/opportunity/c94add13-9be0-4820-b4c4-9b2e5d71f33b',86.00,2,2,'chalet',11631600.00,135251.16,'installment',2326216.00,2025,NULL,NULL,8,4);
/*!40000 ALTER TABLE `property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_amenity`
--

DROP TABLE IF EXISTS `property_amenity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_amenity` (
  `property_id` int NOT NULL,
  `amenity_id` int NOT NULL,
  PRIMARY KEY (`property_id`,`amenity_id`),
  KEY `amenity_id` (`amenity_id`),
  CONSTRAINT `property_amenity_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `property` (`property_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `property_amenity_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenity` (`amenity_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_amenity`
--

LOCK TABLES `property_amenity` WRITE;
/*!40000 ALTER TABLE `property_amenity` DISABLE KEYS */;
INSERT INTO `property_amenity` VALUES (1,1),(2,1),(5,1),(6,1),(9,1),(1,2),(2,2),(3,2),(4,2),(5,2),(7,2),(1,3),(2,3),(6,3),(9,3),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(1,5),(2,5),(5,5),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(3,13),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13),(3,14),(4,14),(5,14),(6,14),(7,14),(8,14),(9,14),(3,15),(7,15),(8,15),(3,17),(4,17),(5,17),(6,17),(7,17),(8,17),(3,18),(4,18),(5,18),(6,18),(7,18),(8,18),(9,18),(5,28),(8,28),(6,38),(9,38);
/*!40000 ALTER TABLE `property_amenity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `development_id` int NOT NULL,
  `rating` int NOT NULL,
  `review_comment` text,
  `review_date` date NOT NULL,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY `user_id` (`user_id`,`development_id`),
  KEY `development_id` (`development_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`development_id`) REFERENCES `development` (`development_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `review_chk_1` CHECK ((`rating` between 1 and 10))
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,118,3,6,'المشروع بيوفّر أمن 24 ساعة وده نقطة قوية. بشكل عام مقبول.','2024-02-03'),(2,66,3,5,'صاحبي اشترى هناك وكان مقبول. أنصح بشدة المشروع ده.','2026-07-11'),(3,171,3,10,'الأمن والخدمات كويسة. التشطيبات تحتاج مراجعة.','2026-01-12'),(4,3,3,8,'تجربة يحتاج تحسين بكل المقاييس — التسليم كان في الموعد.','2024-06-21'),(5,120,3,4,'صاحبي اشترى هناك وكان مقبول. أنصح بشكل عام المشروع ده.','2026-02-26'),(6,74,3,6,'شقة يحتاج تحسين في مشروع جيد جدًا. السعر معقول مقارنة بالمنطقة.','2026-02-08'),(7,174,3,7,'صاحبي اشترى هناك وكان رائع. أنصح مع التحفظ على السعر المشروع ده.','2024-12-17'),(8,166,4,8,'شقة ممتاز في مشروع ممتاز. السعر معقول مقارنة بالمنطقة.','2024-08-15'),(9,17,4,7,'صاحبي اشترى هناك وكان عادي. أنصح بشكل عام المشروع ده.','2026-08-13'),(10,163,4,8,'المشروع بيوفّر أمن 24 ساعة وده نقطة قوية. بشكل عام رائع.','2025-04-02'),(11,119,4,4,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام ممتاز.','2025-08-25'),(12,180,4,3,'شقة مميز في مشروع جيد جدًا. السعر مرتفع قليلًا مقارنة بالمنطقة.','2026-01-26'),(13,78,4,6,'المشروع ده تجربتي معاه كانت عادي. الموقع مميز والخدمات كويسة.','2026-09-17'),(14,68,1,6,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام رائع.','2023-11-17'),(15,14,1,6,'المشروع ده تجربتي معاه كانت رائع. الموقع استراتيجي والخدمات ممتازة.','2024-12-29'),(16,33,1,8,'شقة مقبول في مشروع مميز. السعر منافس مقارنة بالمنطقة.','2026-03-30'),(17,190,1,8,'الأمن والخدمات ممتازة. التشطيبات جيدة.','2024-07-25'),(18,108,1,6,'تجربة رائع بكل المقاييس — التسليم كان قبل الموعد.','2026-04-28'),(19,111,2,6,'صاحبي اشترى هناك وكان ممتاز. أنصح بشدة المشروع ده.','2025-03-09'),(20,25,2,9,'المشروع ده تجربتي معاه كانت مميز. الموقع مركزي والخدمات كويسة.','2024-09-27'),(21,191,2,5,'صاحبي اشترى هناك وكان جيد جدًا. أنصح مع التحفظ على السعر المشروع ده.','2025-01-25'),(22,190,2,10,'تجربة ممتاز بكل المقاييس — التسليم كان في الموعد.','2023-10-29'),(23,97,5,7,'صاحبي اشترى هناك وكان مميز. أنصح بشدة المشروع ده.','2025-04-10'),(24,108,5,7,'المشروع بيوفّر حمام سباحة وده نقطة قوية. بشكل عام مميز.','2026-03-06'),(25,117,5,7,'صاحبي اشترى هناك وكان عادي. أنصح بشدة المشروع ده.','2025-02-09'),(26,88,5,10,'شقة يحتاج تحسين في مشروع مقبول. السعر معقول مقارنة بالمنطقة.','2025-10-25'),(27,41,5,4,'صاحبي اشترى هناك وكان مميز. أنصح بشدة المشروع ده.','2024-03-22'),(28,95,5,10,'تجربة مميز بكل المقاييس — التسليم كان في الموعد.','2025-11-02'),(29,186,3,6,'المشروع بيوفّر أمن 24 ساعة وده نقطة قوية. بشكل عام مقبول.','2024-02-04'),(30,92,3,5,'صاحبي اشترى هناك وكان مقبول. أنصح بشدة المشروع ده.','2026-07-12'),(31,91,3,10,'الأمن والخدمات كويسة. التشطيبات تحتاج مراجعة.','2026-01-13'),(32,34,3,8,'تجربة يحتاج تحسين بكل المقاييس — التسليم كان في الموعد.','2024-06-22'),(33,157,3,4,'صاحبي اشترى هناك وكان مقبول. أنصح بشكل عام المشروع ده.','2026-02-27'),(34,115,3,6,'شقة يحتاج تحسين في مشروع جيد جدًا. السعر معقول مقارنة بالمنطقة.','2026-02-09'),(35,62,3,7,'صاحبي اشترى هناك وكان رائع. أنصح مع التحفظ على السعر المشروع ده.','2024-12-18'),(36,184,4,8,'شقة ممتاز في مشروع ممتاز. السعر معقول مقارنة بالمنطقة.','2024-08-16'),(37,75,4,7,'صاحبي اشترى هناك وكان عادي. أنصح بشكل عام المشروع ده.','2026-08-14'),(38,195,4,8,'المشروع بيوفّر أمن 24 ساعة وده نقطة قوية. بشكل عام رائع.','2025-04-03'),(39,86,4,4,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام ممتاز.','2025-08-26'),(40,48,4,3,'شقة مميز في مشروع جيد جدًا. السعر مرتفع قليلًا مقارنة بالمنطقة.','2026-01-27'),(41,130,4,6,'المشروع ده تجربتي معاه كانت عادي. الموقع مميز والخدمات كويسة.','2026-09-18'),(42,148,1,6,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام رائع.','2023-11-18'),(43,95,1,6,'المشروع ده تجربتي معاه كانت رائع. الموقع استراتيجي والخدمات ممتازة.','2024-12-30'),(44,84,1,8,'شقة مقبول في مشروع مميز. السعر منافس مقارنة بالمنطقة.','2026-03-31'),(45,15,1,8,'الأمن والخدمات ممتازة. التشطيبات جيدة.','2024-07-26'),(46,80,1,6,'تجربة رائع بكل المقاييس — التسليم كان قبل الموعد.','2026-04-29'),(47,139,2,6,'صاحبي اشترى هناك وكان ممتاز. أنصح بشدة المشروع ده.','2025-03-10'),(48,85,2,9,'المشروع ده تجربتي معاه كانت مميز. الموقع مركزي والخدمات كويسة.','2024-09-28'),(49,6,2,5,'صاحبي اشترى هناك وكان جيد جدًا. أنصح مع التحفظ على السعر المشروع ده.','2025-01-26'),(50,15,2,10,'تجربة ممتاز بكل المقاييس — التسليم كان في الموعد.','2023-10-30'),(51,197,5,7,'صاحبي اشترى هناك وكان مميز. أنصح بشدة المشروع ده.','2025-04-11'),(52,80,5,7,'المشروع بيوفّر حمام سباحة وده نقطة قوية. بشكل عام مميز.','2026-03-07'),(53,166,5,7,'صاحبي اشترى هناك وكان عادي. أنصح بشدة المشروع ده.','2025-02-10'),(54,101,5,10,'شقة يحتاج تحسين في مشروع مقبول. السعر معقول مقارنة بالمنطقة.','2025-10-26'),(55,132,5,4,'صاحبي اشترى هناك وكان مميز. أنصح بشدة المشروع ده.','2024-03-23'),(56,40,5,10,'تجربة مميز بكل المقاييس — التسليم كان في الموعد.','2025-11-03'),(57,59,6,4,'شقة رائع في مشروع عادي. السعر منافس مقارنة بالمنطقة.','2025-12-02'),(58,173,6,2,'صاحبي اشترى هناك وكان مقبول. أنصح بشكل عام المشروع ده.','2026-03-17'),(59,41,6,5,'صاحبي اشترى هناك وكان مقبول. أنصح مع التحفظ على السعر المشروع ده.','2026-07-13'),(60,160,6,10,'الأمن والخدمات كويسة. التشطيبات تحتاج مراجعة.','2026-01-14'),(61,33,8,8,'صاحبي اشترى هناك وكان مقبول. أنصح بشدة المشروع ده.','2026-01-24'),(62,184,8,9,'صاحبي اشترى هناك وكان مميز. أنصح بشكل عام المشروع ده.','2026-05-20'),(63,121,8,4,'الأمن والخدمات تحتاج تطوير. التشطيبات جيدة.','2026-02-10'),(64,185,8,7,'صاحبي اشترى هناك وكان رائع. أنصح مع التحفظ على السعر المشروع ده.','2024-12-19'),(65,184,1,8,'شقة ممتاز في مشروع ممتاز. السعر معقول مقارنة بالمنطقة.','2024-08-17'),(66,75,1,7,'صاحبي اشترى هناك وكان عادي. أنصح بشكل عام المشروع ده.','2026-08-15'),(67,195,1,8,'المشروع بيوفّر أمن 24 ساعة وده نقطة قوية. بشكل عام رائع.','2025-04-04'),(68,86,1,4,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام ممتاز.','2025-08-27'),(69,48,1,3,'شقة مميز في مشروع جيد جدًا. السعر مرتفع قليلًا مقارنة بالمنطقة.','2026-01-28'),(70,130,1,6,'المشروع ده تجربتي معاه كانت عادي. الموقع مميز والخدمات كويسة.','2026-09-19'),(71,148,7,6,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام رائع.','2023-11-19'),(72,95,7,6,'المشروع ده تجربتي معاه كانت رائع. الموقع استراتيجي والخدمات ممتازة.','2024-12-31'),(73,84,7,8,'شقة مقبول في مشروع مميز. السعر منافس مقارنة بالمنطقة.','2026-04-01'),(74,15,7,8,'الأمن والخدمات ممتازة. التشطيبات جيدة.','2024-07-27'),(75,80,7,6,'تجربة رائع بكل المقاييس — التسليم كان قبل الموعد.','2026-04-30'),(76,139,4,6,'صاحبي اشترى هناك وكان ممتاز. أنصح بشدة المشروع ده.','2025-03-11'),(77,85,4,9,'المشروع ده تجربتي معاه كانت مميز. الموقع مركزي والخدمات كويسة.','2024-09-29'),(78,6,4,5,'صاحبي اشترى هناك وكان جيد جدًا. أنصح مع التحفظ على السعر المشروع ده.','2025-01-27'),(79,15,4,10,'تجربة ممتاز بكل المقاييس — التسليم كان في الموعد.','2023-10-31'),(86,163,2,7,'الأمن والخدمات كويسة. التشطيبات تحتاج مراجعة.','2025-09-19'),(87,67,2,10,'تجربة مقبول بكل المقاييس — التسليم كان في الموعد.','2025-12-12'),(88,135,2,8,'شقة يحتاج تحسين في مشروع عادي. السعر جيد مقارنة بالمنطقة.','2024-12-29'),(89,162,2,9,'شقة رائع في مشروع ممتاز. السعر منافس مقارنة بالمنطقة.','2023-12-17'),(90,112,2,2,'المشروع بيوفّر حمام سباحة وده نقطة قوية. بشكل عام ممتاز.','2023-12-18'),(91,82,2,6,'المشروع بيوفّر جيم وده نقطة قوية. بشكل عام يحتاج تحسين.','2026-03-24'),(92,146,2,9,'الأمن والخدمات عالية المستوى. التشطيبات جيدة.','2023-11-16'),(93,182,2,9,'تجربة مقبول بكل المقاييس — التسليم كان قبل الموعد.','2026-04-11'),(94,123,2,9,'تجربة مقبول بكل المقاييس — التسليم كان قبل الموعد.','2024-08-10'),(95,158,2,4,'تجربة مميز بكل المقاييس — التسليم كان قبل الموعد.','2026-09-14'),(96,185,3,10,'شقة ممتاز في مشروع مقبول. السعر منافس مقارنة بالمنطقة.','2025-12-10'),(97,97,3,4,'الأمن والخدمات تحتاج تطوير. التشطيبات جيدة.','2024-04-15'),(98,141,3,4,'تجربة يحتاج تحسين بكل المقاييس — التسليم كان قبل الموعد.','2025-03-23'),(99,101,3,9,'شقة يحتاج تحسين في مشروع جيد جدًا. السعر معقول مقارنة بالمنطقة.','2026-03-25'),(100,194,3,8,'تجربة ممتاز بكل المقاييس — التسليم كان قبل الموعد.','2025-07-24'),(102,32,3,6,'الأمن والخدمات كويسة. التشطيبات تحتاج مراجعة.','2024-03-05'),(103,183,3,6,'المشروع ده تجربتي معاه كانت ممتاز. الموقع مركزي والخدمات كويسة.','2026-02-14');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `user_chk_1` CHECK ((`gender` in (_utf8mb4'Male',_utf8mb4'Female'))),
  CONSTRAINT `user_chk_2` CHECK ((`age` >= 18))
) ENGINE=InnoDB AUTO_INCREMENT=601 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'johnsonjoshua','donaldgarcia@example.net','5280379e480d19186230dc72c4b97720212449dc0e13bdbec00bf74cd4daf7c5','Male',20,'2006-07-28'),(2,'garzaanthony','robinsonwilliam@example.org','383efa3d58e7ffa6680f39ab0c7907a65b4967b8a00485566846b4a12c160b56','Female',39,'1986-11-05'),(3,'jennifermiles','lrobinson@example.com','3e66ad21aaf9b78262a838c60958b9b189ccda4eb9da24c48106c49ffa7130db','Male',30,'1996-04-18'),(4,'blakeerik','jpeterson@example.org','e82d2c8194c2f6d0dba417c1719d43369f76c288dbb1d68ebfee411a682830b1','Male',66,'1959-11-21'),(5,'curtis61','melanie94@example.org','47182287ce16d512a6f9f653770247b3968e5d6b6aaf5944841553ada73a8b4e','Male',55,'1970-12-18'),(6,'yherrera','arnoldmaria@example.net','97dcf9a6cf2c8aed9c5cb9ed003be8ff5a9a768d42c8a61e6addb1195166ded9','Male',20,'2006-02-21'),(7,'barbara10','kendragalloway@example.org','9a26db757254c52658c80ecb4352208c23ed166e79258be268cab09cda715e89','Male',37,'1989-03-14'),(8,'jamesshawn','francisco53@example.net','125ee5f931f1100ecea244707756bd179ecf28f41f0caffd981f8eb0c85af2de','Male',63,'1963-06-24'),(9,'jacqueline19','amandasanchez@example.com','4b094a8866b926609443790db87b19de00a53e9d48a08a66fd99a800ff65abfe','Male',68,'1958-06-19'),(10,'onelson','gabriellecameron@example.org','7d58786818250f23de0277b64c966d20d6ebf6b02688679a73cc2b56cd67ea43','Male',66,'1959-12-05'),(11,'lydiatrujillo','nadams@example.net','a92e8b629234e57aa5405d281f581ff1e6e323aff988036a45853fa48ba7a77f','Female',37,'1989-01-14'),(12,'jason76','ithomas@example.org','1e4b1c1420240f60f819828383384f2ae6caa8469b81392a0dc3a49533a1825a','Female',42,'1983-11-10'),(13,'julie69','icox@example.net','4ee7b0e23a047eafcbc29671a5254e28354e15af268cfab455a279493530f7ca','Male',32,'1994-06-29'),(14,'ddavis','hernandezernest@example.net','eaa36bf11c33a383b055e122e02c6d2425d178e73e089f43cec1a211057e5ef9','Female',48,'1978-04-16'),(15,'ycarlson','dcarlson@example.net','f4d30924391fe7e3b2fdd5ab925b611e6e8f5f28ac1084eee294edd3733aee64','Female',31,'1994-11-13'),(16,'tasha01','kayla51@example.com','c002ca9907e289b0b9503afb9930f770c112a0d6c79b01bf8b1c45cc6b3a9d05','Male',48,'1978-08-14'),(17,'amoore','teresa28@example.org','d6666790f57ba9f8c2cf8f4ca238fde7a998b02e484ba9a17a0f7c2bdefef14d','Male',26,'2000-06-29'),(18,'meagan89','ericfarmer@example.net','6533a41d30c32aa25469f5facd031c13841ca0744a403a60fe19b843ea2fbd19','Female',26,'2000-02-20'),(19,'georgetracy','hickmannatasha@example.com','bb600a443bd59c9277c6f18ad7322812f491c05ac5b2c9e43e481499006cf691','Female',48,'1977-12-16'),(20,'brianhumphrey','millertodd@example.org','fe766d1f95711695c7a0657a9e435c8521dd6e7d7f1a5afa3f0a166447c05c39','Female',21,'2004-12-01'),(21,'davidalvarez','josephbrennan@example.com','a49897f465403d23a883fe84cf445f64fee69f3e60bf9a216a6ab5b2f6a92415','Female',66,'1960-09-15'),(22,'sarahcampos','jenniferross@example.net','df71fd9b82962556d076648a09cf3a54bf951d52e104a2c3135c3a3646594486','Male',51,'1974-11-09'),(23,'samuel87','wrightcaleb@example.org','c15416d8d48aded638a0f3c470c91122508681081f17d9e7d1d11dff803d988b','Male',67,'1959-04-16'),(24,'briannasmith','perezrebecca@example.com','8d9b45abf1902b16ba54e033e6ea026db86a355f20cf6ed0f4607da4e31c8669','Female',50,'1976-05-15'),(25,'palmerjoshua','ilewis@example.net','dafd4a6baa65bde21c7721426e1639faead742739e823d0949bd8f51e8475605','Male',24,'2002-07-29'),(26,'esanchez','glee@example.net','3416810399828643ee94339267e23ec0b94279ff0351b43e7f62f5b5306c8817','Male',38,'1988-05-15'),(27,'agomez','dshields@example.net','ae1741384bf47efdf57256c6c8627151501ebbd8c84bc498422f69d2a1904faf','Female',25,'2001-08-28'),(28,'brownjessica','wrightjames@example.com','11ba1ebc8c63c72395fb48a5dd1d99bd2525fd32798162ffc87e529038915ccd','Male',27,'1999-10-03'),(29,'robertramirez','nancyjones@example.net','06bcab32f2b58e0e81dd60ad19c5515146a6aafd5315ae402c3c0628a8889b56','Female',42,'1983-11-17'),(30,'williamsyvette','novaksara@example.org','1c6572024b0eda9982ee926a793ea22bb4bbc52a072dff78b909089558ee6d36','Female',50,'1976-02-01'),(31,'richardolson','kbarrera@example.com','e050dbf65ca504576d8dfb7a98349cf8ae98218ebbc92242ca25b9cc0036b8b0','Male',51,'1975-08-09'),(32,'gallowayjoseph','smitchell@example.net','1b1bfc8523deb9ec741983b968e60437caf57b8591e86a750db7698cd11fee95','Female',36,'1990-01-07'),(33,'smoore','tanyariley@example.net','c2e6ad27d11bf7aa919d32b3411f27940babe8c5927ad666ac103bd3589a669d','Female',24,'2002-05-30'),(34,'adkinsbrian','hshaw@example.org','5a7846fff6b03c92f772b8d27bf0ad08d0a1eee2f6b622677163a9aa4e1c61cf','Male',65,'1960-11-23'),(35,'yuchristopher','caseyjones@example.org','465d71047fb37d6b0225d4002a9080ba060f734e74252aa43624296fec56fbaa','Male',32,'1994-02-26'),(36,'kwilson','bethwilliams@example.org','9882d3b83295ad69c2782be2b4cbe14a48bb3494f521484e757b47f9503b38a3','Female',52,'1974-10-10'),(37,'ksandoval','sarah35@example.org','4ad03e9dd7a4865c58455f53062f9bb61aa11a2d701e8aeaacb3202c46747b7c','Female',68,'1958-11-06'),(38,'randy47','sarah10@example.com','ce8a6c457d4b7d2b905c9e8595ff5f64d8d580c8c8180e4b6d545d998cbd21a0','Male',47,'1979-09-21'),(39,'jonesjason','david51@example.org','859c0ba80c6b6bcd819a738f27f94bd8a9402ba40920ba6d946856000efc9e68','Male',38,'1988-04-07'),(40,'justin78','cheryl80@example.net','f594385d24a6d72a1de55f7caac74233b50e9acfa9496f9ffcc8ead350b69d88','Male',46,'1980-07-07'),(41,'sarah12','darrell18@example.org','e534feefea6095aa7f021f6c537c7411fca4672c13fc3d688ee7cb46f133214e','Female',42,'1984-10-17'),(42,'juan35','gracefarrell@example.net','9f4fcfd73168f196fcc5b7808d0ad68a935507354ec56d972fd5350780c63d5e','Male',36,'1989-11-20'),(43,'dking','waltersmaria@example.org','3159488f61132ec1cb0c9674926d0e370407c6c6ae5792aed978e81cf338b68d','Female',37,'1989-09-27'),(44,'cookdavid','evan78@example.net','1fa0a8aa9c200502789c3db8b0f58b2590ca0073ebe44e98c199cb58b7489aee','Female',53,'1973-04-27'),(45,'hhoffman','landryhannah@example.org','7f8371a8b8cd73a3666ffa6c403d06e03e13cadae95f74e00b4ccf4964be4cb7','Female',30,'1995-12-31'),(46,'davenportbrandi','russellwilliams@example.com','380712ce76b191956d5bac5576664ac0603f93e78977541269bc596cb0a8a9c0','Female',30,'1996-04-15'),(47,'nolanjason','elizabethgomez@example.net','77ab8512f58e632d6edbda5b7ea4ad1765451b6fa611ec409a34d6d1272bf757','Male',68,'1958-06-15'),(48,'vdickson','sarayoung@example.org','9b72c30bf3e8a5e2330b60fa29978e43b39fb614c4226924ce3ba3ea1bd216ce','Female',56,'1970-05-19'),(49,'nicolejohnson','kimberly63@example.com','e56070d70d49ac1646637e64eba7b421b805dc937f19d5acaeae6aee0a74fcdf','Female',50,'1976-05-04'),(50,'kristinrodriguez','garrisonjeffrey@example.com','6c011a38890d2d90f1897c057e9b837442872fa00bb4a6a44661b0bc4e4ff4fa','Male',30,'1996-05-28'),(51,'kevin33','kellerraymond@example.com','d7724bbc00b860531beee0ac4ed7ff47541b90666315ec4043b908833be9c3df','Female',26,'2000-08-29'),(52,'rasmussenjoshua','ifrazier@example.com','3b82036808b2e807ce86ec9624816fa8e590877de87a7e56eeb76a8edf8d7035','Male',27,'1998-12-24'),(53,'wilsontara','beverlyterrell@example.org','46e2860b385acf8029c5a8ff6e2478dbfab6d772fd3ece513220311226c55467','Male',32,'1994-06-18'),(54,'carlsonmichael','samuel81@example.com','9fd38967a2635230eae58e072d082f354d468f2bdc06bd2a36b711d064146cdc','Female',23,'2003-02-12'),(55,'jonathanfletcher','meyerlindsay@example.net','a9ac1952ea1460ca8b012a0bfdaadb08929aab43ecb4eb076bd168cea25380ba','Female',52,'1974-07-31'),(56,'michaeljones','cindy14@example.net','b77d743c62278102edfc52ffcb31d45fb6538d00ac8702f1141037688ca1592f','Female',65,'1961-05-06'),(57,'elizabeth56','angela36@example.net','579fd3826118e254a82d2a86601e592ad0c494c96e0351158a48b9bf3933cc53','Female',67,'1959-03-08'),(58,'lbyrd','richard04@example.com','657e3c04486384b424a9eb88f134e92bdf463f0e865c28932a4270d5aec9b923','Male',28,'1998-07-16'),(59,'russellcarpenter','steven73@example.net','4592d143618947327e81f751d3f7b15cc2852beb7ec6f92ac56de7fa6ef7eff7','Female',48,'1978-04-19'),(60,'yleon','donnacampbell@example.net','58ecd883c8cf9bd20ff2bc6856142a1d936fa9d982e4c336ec7cc26042d05b47','Male',44,'1982-06-26'),(61,'clarence34','lindsayhernandez@example.org','065ba15c8e3b4848c02caa92c79438e3d6160242dadd1c9cb825c11723bee7e9','Female',32,'1994-08-17'),(62,'traceycarr','gibsonolivia@example.net','025b251e87f89eb62740e8a72b1ee5bab4f6ecf7427b64394e0808aea6c694e2','Female',18,'2008-07-10'),(63,'jennifercruz','psanchez@example.net','8babc92f22f55a7fd65a029f85a44acd5a57e19ba7d689a9d06d2caa27f58266','Female',62,'1963-11-27'),(64,'staffordmichelle','osbornejeffery@example.net','07bbbb5604ddbabe1f9fe80ee56cf0f10cd2e823a8fe16674172d03770cc100d','Male',63,'1963-04-09'),(65,'pwilliams','bryantlaurie@example.net','0352b5a01f2f121a88268e1119b8b480aa780e621eed13212a92b931e464fb7f','Male',44,'1982-01-15'),(66,'stephanie79','jrivas@example.com','71f54609e1de0466cbe59e724fa3ed01551b6bf4df95bc69e7d5289f82e4f55f','Male',31,'1995-02-07'),(67,'juliawells','karen48@example.com','1df821c3a29c2a06bd9c945fc409a57434cc4a7ac3b2ba62dc893e5a59e05949','Female',32,'1994-04-28'),(68,'joshuajones','jimmy55@example.net','10b3cf1c3d91dbc2ff19c74ebb7c4806f1e9a84b14aedde48145856223dd9768','Male',47,'1979-09-26'),(69,'taylorjesse','jasminebrown@example.com','f787fb4f0f9a547b86c3bcbff3da28314761a66a29b3dc11449fe403dab18fad','Female',19,'2007-01-25'),(70,'amy60','marissaprice@example.net','c2ee812baa47a78238663906e3fc58f0fb52cd3f00c3ff58337c5b9087a029cc','Male',50,'1976-04-01'),(71,'gateskathy','wwoods@example.com','3ea35af062af0abccb46d0844ef631c0ad5f363efad91df09611cb1a0596d352','Female',39,'1987-05-02'),(72,'acastaneda','tracynelson@example.com','02e8ab10f30c0ee3abf9ee1a67b4a2926180874aeb061ef3c067f7e5ca5a963c','Male',39,'1987-03-17'),(73,'priceelizabeth','dramsey@example.org','1060e08297d2145cc65d24e3d19132b513c074362b66c8600abf646e794b24e2','Male',25,'2001-02-17'),(74,'meadowsbrittany','millerroy@example.com','cb3a031b3a3a35e711972f4fd492292af4f569a633f58da504155ba9f3a2f37e','Female',24,'2002-08-10'),(75,'brentgray','shawnrogers@example.com','1c20d32620919f742961463a5ba7947f8b7849c23fa15a2abd2c334b7e0b4a1c','Male',29,'1997-04-18'),(76,'karen64','ruizkaitlyn@example.org','21306f8618f0608a819dbe88ac54fc58b35048da062d114e9d4d3111e4493a3f','Female',67,'1959-06-29'),(77,'jeffrey10','herringjames@example.org','727bdbb911eacf00ed67d928a5ca837469dc584871d107155da5fa3deb8d14cd','Male',41,'1985-01-13'),(78,'johnwells','elliottjeffery@example.net','632c9f6c1f081236c03190f459264496b144352cbb66a08e96213da10c361f53','Female',37,'1989-10-24'),(79,'katie29','stricklandfrank@example.com','544baa9ac5800ba4580c13e80db1bcba3967d156fc9c6d647822d8fe3eaf4315','Male',45,'1980-11-06'),(80,'lanesarah','tsanders@example.org','96823227c0753bbc496e9058511fa1740bc584056e7165b103c8a339ada18791','Female',51,'1975-04-25'),(81,'vargasmaria','curtisbarton@example.net','74a131f3748eee3230f49bc08d9c4b9c2be35fd56c64720d0f272757c2412b8b','Female',64,'1962-05-20'),(82,'hoganashlee','reedross@example.com','4bce535d794baddef259f2a3154ab913c5693fe438910d389cb68e0dc2bce4cf','Female',28,'1997-12-16'),(83,'huntermatthew','gshort@example.com','f59077e03c36053d3a04dd9c67a63c5c0e0e02d932f052af38ebd20ecf606913','Male',38,'1988-08-28'),(84,'cynthia72','hthompson@example.net','58b29641d8515077172cdd44d4cf4b8dbff3c0940b5bdfbd85a1a9eb6915cbfe','Male',48,'1978-06-26'),(85,'christina87','ugraham@example.net','32707ab2a5294161d83370bb79ffcf43ea4a04785bb59a6c06eeeea22b9267fb','Male',67,'1959-02-14'),(86,'marcus31','nicole37@example.net','508351d5a7a3211084915a289bf34d1468cf9add46a6a5b8514e48a03883635c','Male',37,'1989-01-21'),(87,'frogers','hunter35@example.com','fcde23f22a192e0d536bc985ed03049eec4516758c4348fb29c7cbc0d16de7c0','Male',24,'2002-06-12'),(88,'joshua94','blackjames@example.org','7eece0809a01e171a90efc5c91f82c94697eb7f81d25c2ead58d33d5d1eddeb8','Male',38,'1988-04-11'),(89,'wfreeman','hannahbrewer@example.com','9979563b979c8a0740d8011c6858cc6a324e5096855e0a44fb8a994c1679a4cb','Male',20,'2005-12-30'),(90,'fmcguire','jeffrey34@example.net','956582927960e8f54287bc80f7adc3f7755f5bfedaad15d4128c26ec0db7a6ff','Female',24,'2002-06-17'),(91,'thomas85','jbarajas@example.com','170687b9894ba1731b6a738c7c4d642a92efcf25afecff1634987340d3f600aa','Male',43,'1983-10-31'),(92,'jacqueline44','jerry35@example.org','8e3c04c353e0304f492d73a56c8645f051d492d6c9c54b88e09b0af888534d21','Female',37,'1989-08-05'),(93,'jamesrodgers','jenny89@example.com','e49d9a5e2ec68da256bf0948bb25f0a4cac172daf5a8d3a3e72003e2c9aa0a09','Male',69,'1957-08-02'),(94,'wallkenneth','harry08@example.org','7b8ce7e8518c5a773f65e1898a4ba561712b84f36db6b879ca6e2d25ca3fdbaf','Female',39,'1987-01-06'),(95,'brandon08','heidi27@example.org','cedfb90cfba2437be91a90dd90bc6c63a1f7f47d4dd60d0eb42bc701475fac3e','Female',54,'1972-04-18'),(96,'andrewstaylor','dpeterson@example.com','46e2812dda578f4f0e21fc51cb455bdfba02cfaf0b1dc13b3760e8ee37ae13b1','Male',26,'2000-05-09'),(97,'ewilson','kvasquez@example.net','d534ffa03192d7e6c19a7c8e71a812703997dff9c275a3a62faf41aabc137818','Male',56,'1970-02-22'),(98,'hernandezlisa','christopher31@example.net','a95114aec202e4c4fd7e8f0ecf2f9816c2dad145314c4336dd961dbbaa80c1ff','Female',56,'1970-10-25'),(99,'yobrien','kimberlyjames@example.com','c25e2b2fbac2609d364bc1156048200e2854dbb3cdeb311a68947cde61773328','Female',59,'1966-12-01'),(100,'michelle64','lynchjody@example.org','86d993d031b3c7c1780f6147b34eec8d4a3e200e3d8846938f7f2a174ae93bed','Male',26,'1999-12-27'),(101,'josephmiller','glennjones@example.org','7de35dec5aaf651a5306d7c1260d17eba1c4d62479916102be3534f7e4208fa0','Male',54,'1972-09-10'),(102,'mhayes','ocarter@example.com','b1fefd7bc95ab76522de71fe95ca1871a1578cd5bdc9402fb3ca9c4edfe10f44','Female',27,'1999-01-05'),(103,'jacqueline71','sandrafrench@example.net','56c4fa2efbdab2b87c36b24120bc6c54ac52562f6816d07f4416ee8416c4ed3d','Male',35,'1991-08-17'),(104,'ronaldstephens','rebekahserrano@example.org','7cdc0b4d7075884b7716c7a1e8054fcbaf5a79a0686b9e25b9a5d66a5a58619b','Male',66,'1960-09-13'),(105,'martinkyle','scott74@example.net','6a8cf731ad238b56306674d2f91695c56c66af5183964d7c050371e99021eb5b','Female',30,'1996-03-28'),(106,'gbender','mkim@example.org','ad87ce68ceeadf4f93b2a370280c730f424d4d7f60180bd4d78ef158362115fe','Female',34,'1992-05-09'),(107,'mnavarro','anthony39@example.net','57b1b9485687854404af37000bdcedf2480bbcd266555b0a8a2e1cc86d276d2b','Female',59,'1967-04-24'),(108,'keyemily','barbara27@example.net','3ec4564c27c013862955787adf37ca82ee34bebff0bedb056c21f9cbda6518a6','Male',24,'2002-01-19'),(109,'lmoon','fwalters@example.org','78c9141a0e0105d8281f5aa6ffbe6b11463120e3b356298a66f053255bbc6e07','Female',67,'1959-06-11'),(110,'vbailey','elizabeth25@example.com','9adc850e1d50a1895fde83bc3d7cf1166c8def00ea0e83cf80845dc9c6d4f91b','Male',22,'2004-04-11'),(111,'zroberts','gibsonleonard@example.com','4bf39eb43e22e6de8cb2f9b92a7d36f57183744c25efe07f55afcbfe1de64deb','Male',26,'2000-06-12'),(112,'cordovarichard','sandovalamy@example.com','7aa98f32773f106d8e105a3922f2ed4895bf703fe96033c3b17a1e81c01d8894','Male',32,'1993-11-23'),(113,'lopezmichael','wgarrett@example.org','28f4a0148e2de1d007dc009703a5f7839925350ae67ec66e1babda71441e495f','Female',61,'1965-03-31'),(114,'josephanderson','samuel71@example.org','81affd57d2c7377dfd438577f5ec40e3f7cb36284bf39c0e6921b619b42a6514','Female',37,'1989-08-21'),(115,'jennifercollins','tranchristopher@example.org','3a29e75de8c84b56b3e2f6133809dad0826f237a66935e4d74bb8996c9d6d4c8','Female',23,'2003-07-22'),(116,'pvalentine','tyronemoran@example.net','9f12412137d6980a45e69b84e03c43bbe81c2c39b1e1cb20c5dcbaeab2847c14','Male',52,'1974-10-25'),(117,'robert77','stephenthomas@example.org','77c2ae048921698d1dface8efda0bb677b4062eaa9130f19454d0351da15ace6','Male',53,'1973-10-15'),(118,'michellehill','ymorgan@example.net','2f4e83337e86988257f7f053b5f60805248476ac1206358d1f37e97e50f97cf4','Female',58,'1967-12-30'),(119,'lori44','cgrimes@example.net','fc91dd1569349e18fe1616808816552d31a44bf6d1ebe2f5ded38df9bab46f83','Female',55,'1970-11-12'),(120,'jreed','ugibson@example.org','cc6a361718ba0f45905608abc142654d654f64914145779f55420e9105d0810f','Female',31,'1994-12-05'),(121,'ashleyhall','vwilliams@example.com','e186518ea180220cd672fd136fa4decc8f18814563578e9a7035103f2fdea799','Male',44,'1982-03-13'),(122,'qhughes','tylerjohnson@example.net','7b0ef578908908f47e654972a7719b4d5dc749e61ceb4d49d2b402e3671bac83','Male',23,'2003-07-27'),(123,'molly71','jsmith@example.com','6cb792c79c78a376977e4ae1bc61fa75ec3aedbbe3a6587d24638d8a5e2700c9','Male',46,'1980-09-05'),(124,'charlesharrington','matthew61@example.com','e4ed5c3300a8d5a090fbe2a763b3c913fcc90874a888000371cdb12afe046a7c','Male',22,'2004-04-25'),(125,'ofinley','cbrennan@example.net','e9e2d4795975fed97dbe059faab356c8fcbbaa25b30876a6d4dfd2fc15afb4b3','Female',63,'1963-09-14'),(126,'younggabrielle','wendy16@example.org','e7524c5cfa3248a07f6101e248f5d2e639aaeb424ce9cd8572f5680cf1e5a015','Male',23,'2003-09-18'),(127,'wallaceheather','williamslaura@example.com','e8af93dd8d0a95c99ff65ed58bf84aed018d5dcef13de1652143ca687909cd59','Male',34,'1992-02-22'),(128,'nicholas23','yknight@example.org','33a197c1d5a67dfbcb78dbab5d92a9766fc1544fc7087f6feadde95d0282c4a4','Male',24,'2002-09-20'),(129,'gregorylynch','pharvey@example.com','0d191e402f846b21ac9599def8a9f22cd0535e7e9453d0a25925f6ee3b3668a1','Male',54,'1972-08-04'),(130,'jesselittle','ascott@example.com','52bbe34b510c0438ef91bed4c936884646765d298dd61db01c413745840cb685','Male',69,'1957-09-15'),(131,'erica21','llandry@example.com','6c98b78e2d824557fb0eebddc5409beda952e822253752d16e2e6df0ee2417ae','Male',69,'1956-11-16'),(132,'dvaughn','james67@example.org','98ad65b2c06cb8a9ff35abfcfd2ca16ceaac7ca74441c14744d237dc6b177d99','Male',25,'2001-06-17'),(133,'patrickhoward','victoria40@example.net','e593909d0d2d218b00c8bf91ae34e085898bdda1ba54f183a57e784c402460cd','Female',68,'1958-02-08'),(134,'khill','lozanojulie@example.com','f5340569a5cc7855cc0c9ad283f77680373389c0efef44db8bda1f80037a4ee2','Female',41,'1985-06-03'),(135,'catherinegomez','christinebyrd@example.net','ecfe8c2f2e75a6604ccbed37b50c70ff2709d700a7391373927886aa0aedab73','Male',46,'1980-08-17'),(136,'courtneyberger','parkerscott@example.net','ee515f390834e45be6084fc9fee8dbfc3550898c4f66069be5a661056a84fd99','Male',41,'1984-12-26'),(137,'jessica14','julie23@example.org','8148f9a19b970f31691cd23f59da7d0df3cc5bba7bccd8363765292ac020cab0','Female',29,'1997-01-27'),(138,'alyssa42','robin74@example.net','ab67b8188893e8a9ac33fb09ad34d408a69873ac49daf4406c69597421f08f5a','Female',59,'1967-10-18'),(139,'linda71','karenperez@example.net','0a17a97659cfe8cde6a3f6e824bf540159bd5c8663298b04b0070e2154905adf','Female',24,'2002-04-22'),(140,'zcoffey','christopher60@example.com','7540ac9104f69ae5ac022121ec6dc4920d67685c951d9af79cdd10f9891e3478','Male',59,'1967-09-13'),(141,'gibsonemily','brenda51@example.net','3560f1430a9734729b668ccbcad071b1f0c772697a390b8db477059e795b7bf4','Male',24,'2002-03-30'),(142,'thomasharvey','rose31@example.net','7c33e7ddefff15470b9c25be20b6eb3a3d53632abb43dd06b5ebdd72a5eae288','Male',63,'1963-06-07'),(143,'tblankenship','cwilson@example.org','358f7718630d92c2183e5684e3823e9db5a70e59be982044a64c14173bf83d31','Female',29,'1996-12-06'),(144,'wendy11','paigetaylor@example.com','42c712834c01bf2b03cb8ecfaa1a1ba606782f222ce0ecc11aef46c329486541','Female',24,'2002-08-23'),(145,'ellen86','nicolepena@example.com','be92f821a4d01e625d939b750d6379fa8590750d2541b4d80cc559252cb37bc4','Male',51,'1975-08-31'),(146,'rcrosby','vaughnjeff@example.com','1752e607d5f67dc80ad714f6338351816e0195ab6f1919b7f351b33a7a571073','Female',32,'1994-08-30'),(147,'melissagarcia','amy50@example.com','12d4dd7eb35113b443c7bd92ac80fb38a01d59e3f461610f05839b681d3a59fc','Female',66,'1960-01-30'),(148,'james17','batesdarlene@example.net','47cd23d3e255bc502941ea41a0dbdb83e6477f8bdc06aa0a927ec37983a30ca6','Female',65,'1961-05-12'),(149,'williamsmatthew','kristinharris@example.net','5f936ad406fc7c8a761f5a106e1c452c7b55b4dddad0421a247009b5882344b5','Male',67,'1959-01-22'),(150,'brendali','markhernandez@example.net','159b94229489a94ba15fa009cf2b15bacca63a55de301287a410ccc90555ae22','Female',27,'1999-07-10'),(151,'ramireztracey','amberlindsey@example.org','2ec66c9215cb22e28a8f651455757be28150ed3cb1431f814a218bc9bc33fd87','Male',41,'1985-02-01'),(152,'andersonmichael','briannasmith@example.com','5f71445e68a546e2b8bf5080cedc74fbfde0aa0d2c85178753b2702634060e13','Male',27,'1999-03-19'),(153,'martinezrobert','reesethomas@example.com','4cddb62e7633f4e9cbaf54c7161a5cda4bca08bde8c77293576742819cd59de7','Male',42,'1984-05-19'),(154,'hayesjeffrey','acostaregina@example.net','fea31c7343e68c12c152ff4975a3d401d93dffcca574ee20a7420c34f69c46fe','Female',36,'1989-12-02'),(155,'stephen00','bboone@example.net','63e88bbac499f4e5d619a58a592c9d66b331c70bff82e3bc48ab0d5ddc4c1c4a','Female',36,'1990-07-20'),(156,'henryrenee','lammarc@example.org','1ae904cf295446858ea751a5efc917b7be5efaa786e98b9a195960ea83ff6fe6','Female',63,'1963-06-22'),(157,'martinezclaudia','oscar98@example.com','babc2f102aa775fb92303c23e5f25beaca2023cc98686a738ac9d48d2db2077f','Female',40,'1986-04-15'),(158,'bwagner','mcguiredanny@example.net','d6b7f2bd7aea6317eae4670abccec5d38302bcf74c99b2229581dbaf8bf5e3a0','Male',26,'2000-07-14'),(159,'russellbeasley','dmorgan@example.com','049d7a24dae792d0c29996ba9c9d62023647ea2abb30a0d1f89b91dbc8f0941d','Female',42,'1983-12-29'),(160,'ublair','qedwards@example.com','4585db532a984f84301eea6de39a1c686b0b4d6d61fa9287aebac64fff52e68e','Male',18,'2008-06-30'),(161,'gloriawells','deckerchristopher@example.org','072450178ad87a0866c00e77c02aca4abb343fe05f2dd902ac6cb703c7e3e47d','Female',29,'1997-01-29'),(162,'lisa80','elizabeth65@example.net','2a00e108218dfddcdae17673a5afc0f7e990120380eaf09945115b19bc04132e','Female',32,'1994-04-27'),(163,'uparrish','schmittcaroline@example.com','fa08aa12433705c1e7d46d0dba1c75285df8f57dbd694298eb165cb5f7a9bc59','Female',67,'1959-04-28'),(164,'lanejason','gwalker@example.com','d599976d8f8ee593472402ebb9ffd98d4cb0f24ad12940864dd09c6353d50da9','Female',68,'1958-06-30'),(165,'danny49','lindsaybruce@example.net','58ab85393699356f07dc7e54406bc17a2f4b922019b571413011dada42659d3a','Male',28,'1998-10-12'),(166,'lynchdiane','anthony44@example.com','1cd6d305333275d49dd8796dcee5bfa8bacbf4911d3d4854bbe110893e6c827c','Male',31,'1995-06-11'),(167,'adam29','vjones@example.net','2ff956f5f464de13454ae8c14eaa8757203b1ba7066960ba02d0524460b1c0e3','Male',51,'1975-09-10'),(168,'davisalyssa','vbarnes@example.org','74005c7ad25830eb8836d66fe8a6d103b91ddd8687852d2137f69579e6a40968','Male',56,'1970-04-04'),(169,'larry59','wareeric@example.net','03fe77ef73e441f6cf9cc4d0297841d8e303c139c760e0c9e0b00cfd98f20aa8','Male',21,'2005-01-23'),(170,'craigjoseph','ctucker@example.com','8674d13974d66c321000db15f745423a4540c6ef3b7e1a397b7cf6b0684c11d4','Female',50,'1976-02-07'),(171,'jason81','russell49@example.com','58f220a7059cd729d30cdfc938b6b9624445e4eafc9fab653f8b7f9128552314','Male',50,'1976-09-18'),(172,'brandon69','smithkevin@example.org','e09288a8f947a20be762300d987fc8d81d40be4a63674822f415086ce7bc10e6','Male',40,'1986-06-06'),(173,'kathrynroberts','smithjulie@example.org','f1d22bf59499c90edfcfa55e6f9ed1a993df334f8f199cc378dfe7714f49ed5d','Male',49,'1977-01-31'),(174,'omarpadilla','charles06@example.org','e131ddc60ccbb613ea4bef67c6f49a8d83219881746aa1a568f1593e3cb1234e','Female',31,'1994-12-13'),(175,'umorse','tberry@example.net','b8eea2484915804017ba556edeb7620113cbd4d5affc96cd82af42b8f751adc7','Male',32,'1994-03-28'),(176,'zroberts1','burchgeorge@example.net','67a054f818b0da94b522167f3dedc8979e0822e8777559619c5b01e391a3b4a1','Male',55,'1971-10-29'),(177,'xcollier','kimdaniel@example.com','a9a6cf2aa9190eac7b4682b42853f64ecc02c84e062d65b9e86667b3a080e7ba','Male',34,'1992-09-21'),(178,'zwarren','julie35@example.org','74c8e213effb0f8615b07290f4a8bbc5a17cb1e974427132d45ba1aa21724d34','Female',54,'1971-11-17'),(179,'dixondaniel','rebeccabailey@example.net','2d88e58276a7e2947e8d8778bdfc105ea9bdd29ba8a333f2b51fff7edf58414a','Male',41,'1984-11-17'),(180,'joelthomas','glennhernandez@example.net','a50dbd790ece3e53447ce2819c6457a97200d2e97f66dbd97ab53a632e70f997','Male',27,'1999-02-12'),(181,'thompsonkendra','kmarshall@example.net','d89de011b8c4aad5e68baec8bcb6e5ca9d36898236c27d1742a8fe12c46ed313','Female',21,'2005-05-05'),(182,'kmaldonado','michelle52@example.com','fac73134cb5bd198d15f3086eb838e2dfb42bdef53b35c15c7a931cfef1414ba','Female',37,'1988-11-10'),(183,'harrisoncrystal','brittany58@example.org','db0377264bf4f9741b35d5e88faaa3f488bfa0be724a6d8e1529e234119a886d','Male',59,'1967-07-09'),(184,'steven00','marie11@example.net','a1775dbf7fe1632a774e807512458fe082e52543234a445df98b86fa01d92eb9','Female',45,'1981-06-08'),(185,'jford','colelisa@example.net','324070e452ee70c81386fc9abcc0d491cf5b5500e9348fb655fe8735e41db638','Male',38,'1988-10-25'),(186,'marcalvarez','susanhayes@example.com','315da18f10cc97f56c3b24b407b701a72f470fe4fa12eff35d460d6d225c7c3e','Male',35,'1991-06-28'),(187,'wagnergerald','jasmineritter@example.net','15bac3912629ab1d124556f1ad95a3dcb8a2a7c6777788fa0e40b2ea8b88bf79','Female',47,'1979-05-14'),(188,'michaelhardin','vortiz@example.net','570e4f00ac240dc0c28d177dc662351182d329f9f1efee52834850bb22500aab','Female',24,'2002-08-03'),(189,'mccormickdeborah','riveraangela@example.com','15f92d0f0ad198651043d4186b3c8c098140c3c6f52c94f7259a91815db5b063','Female',49,'1977-04-24'),(190,'johnathan92','christopher25@example.com','0da9c87de971ece35fcf22a72f5500d128bfb3a8f1e0538cb48725728eb2ca83','Female',66,'1960-09-16'),(191,'tanderson','collinsnicholas@example.com','6a401408ef652ccaabc0b6262b6a6151b8cfe644dfe95dc5a5507c0557c51191','Female',20,'2006-05-04'),(192,'elizabethcalderon','lucasrodney@example.com','8eee8983fdc0173e45a82b14ad704e4ac3210f6053933052228969d150b084e6','Male',41,'1985-05-19'),(193,'coxhenry','matthewmiranda@example.org','bdae238fe5d6da041eee2e7ec9a66d98125012f8d4e7518d79a477b7f8165227','Male',41,'1984-12-31'),(194,'zoemoore','megan18@example.net','e6aeeda9dbf4759dc36510276fc2e2ae60a0a734736f19ad394d4e40ba9abe81','Male',27,'1999-02-02'),(195,'stanleynancy','carlamoore@example.org','6dba33e3dd2f34c585497c974188f0417c47283a4391f9df9f281f31191011aa','Female',49,'1977-10-20'),(196,'jenniferwilliams','erica37@example.net','fb64906ead98db060e3932c33009cf8a2c449cb66e4614f989ff266e0133ab69','Female',57,'1969-08-31'),(197,'karen73','kylestokes@example.com','b52f505d60b14d228adcfb558dc8beb46c76af36cd8a4e8cfe980c7a80a36820','Male',52,'1974-04-04'),(198,'michealvalentine','smurray@example.com','742ea2139ac6e409bf84cb09c2c48abd7edaab9a5ad8affca071a0994f3f0a50','Male',40,'1985-12-18'),(199,'mburch','moniquewilliams@example.com','255db96c6e4fc1bf5a053254c62ba2aec86bad54a028b18b9dc1128a12d7b22e','Male',57,'1969-09-11'),(200,'angela18','mitchellkathryn@example.com','c8349c343d44d1969e18f38fa1571793a37c00652efdf01a5fd65f1f45ca01e1','Male',64,'1962-03-04');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_focus_area`
--

DROP TABLE IF EXISTS `user_focus_area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_focus_area` (
  `user_id` int NOT NULL,
  `location_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`location_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `user_focus_area_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_focus_area_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_focus_area`
--

LOCK TABLES `user_focus_area` WRITE;
/*!40000 ALTER TABLE `user_focus_area` DISABLE KEYS */;
INSERT INTO `user_focus_area` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1),(21,1),(23,1),(24,1),(25,1),(26,1),(27,1),(28,1),(29,1),(30,1),(31,1),(32,1),(33,1),(34,1),(35,1),(36,1),(37,1),(38,1),(39,1),(40,1),(41,1),(42,1),(43,1),(44,1),(45,1),(46,1),(47,1),(48,1),(49,1),(50,1),(51,1),(52,1),(53,1),(54,1),(55,1),(56,1),(57,1),(58,1),(59,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1),(71,1),(72,1),(73,1),(74,1),(75,1),(76,1),(77,1),(78,1),(79,1),(80,1),(81,1),(82,1),(83,1),(84,1),(85,1),(86,1),(87,1),(88,1),(89,1),(90,1),(91,1),(92,1),(93,1),(94,1),(95,1),(96,1),(98,1),(99,1),(100,1),(101,1),(102,1),(103,1),(104,1),(105,1),(106,1),(107,1),(108,1),(109,1),(110,1),(111,1),(112,1),(113,1),(114,1),(115,1),(116,1),(117,1),(118,1),(119,1),(120,1),(121,1),(122,1),(123,1),(124,1),(126,1),(127,1),(128,1),(129,1),(130,1),(131,1),(132,1),(133,1),(134,1),(135,1),(136,1),(137,1),(138,1),(139,1),(140,1),(141,1),(142,1),(143,1),(144,1),(145,1),(146,1),(147,1),(148,1),(149,1),(150,1),(151,1),(152,1),(153,1),(154,1),(155,1),(156,1),(157,1),(158,1),(159,1),(160,1),(161,1),(162,1),(163,1),(164,1),(165,1),(166,1),(167,1),(169,1),(170,1),(171,1),(172,1),(173,1),(174,1),(175,1),(176,1),(177,1),(178,1),(179,1),(180,1),(181,1),(182,1),(183,1),(184,1),(185,1),(186,1),(187,1),(188,1),(189,1),(190,1),(191,1),(192,1),(193,1),(194,1),(195,1),(196,1),(197,1),(198,1),(199,1),(200,1),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(15,2),(16,2),(17,2),(18,2),(19,2),(20,2),(22,2),(23,2),(24,2),(25,2),(26,2),(27,2),(28,2),(29,2),(30,2),(31,2),(32,2),(33,2),(34,2),(35,2),(36,2),(37,2),(38,2),(39,2),(40,2),(41,2),(42,2),(43,2),(44,2),(45,2),(46,2),(47,2),(48,2),(49,2),(50,2),(51,2),(52,2),(53,2),(54,2),(55,2),(56,2),(57,2),(58,2),(59,2),(60,2),(61,2),(62,2),(63,2),(64,2),(65,2),(66,2),(67,2),(68,2),(70,2),(71,2),(72,2),(73,2),(74,2),(75,2),(76,2),(77,2),(78,2),(79,2),(80,2),(81,2),(82,2),(83,2),(84,2),(85,2),(86,2),(87,2),(88,2),(89,2),(91,2),(92,2),(93,2),(94,2),(95,2),(96,2),(97,2),(99,2),(100,2),(101,2),(102,2),(103,2),(104,2),(105,2),(106,2),(107,2),(108,2),(109,2),(110,2),(111,2),(112,2),(113,2),(114,2),(115,2),(116,2),(117,2),(118,2),(119,2),(120,2),(121,2),(122,2),(123,2),(124,2),(125,2),(126,2),(127,2),(128,2),(129,2),(130,2),(131,2),(132,2),(134,2),(135,2),(136,2),(137,2),(138,2),(139,2),(140,2),(141,2),(142,2),(143,2),(144,2),(145,2),(146,2),(147,2),(148,2),(149,2),(150,2),(151,2),(152,2),(153,2),(154,2),(155,2),(156,2),(157,2),(158,2),(160,2),(161,2),(162,2),(163,2),(164,2),(165,2),(166,2),(167,2),(168,2),(169,2),(170,2),(171,2),(172,2),(173,2),(174,2),(175,2),(176,2),(177,2),(178,2),(179,2),(180,2),(181,2),(182,2),(183,2),(184,2),(185,2),(186,2),(187,2),(188,2),(190,2),(191,2),(192,2),(193,2),(194,2),(195,2),(196,2),(197,2),(198,2),(199,2),(200,2),(1,3),(2,3),(3,3),(5,3),(6,3),(7,3),(8,3),(15,3),(17,3),(21,3),(22,3),(25,3),(26,3),(27,3),(31,3),(32,3),(34,3),(37,3),(39,3),(40,3),(41,3),(42,3),(46,3),(47,3),(49,3),(50,3),(51,3),(54,3),(55,3),(56,3),(59,3),(61,3),(62,3),(63,3),(67,3),(69,3),(71,3),(72,3),(78,3),(79,3),(80,3),(81,3),(82,3),(84,3),(86,3),(88,3),(90,3),(94,3),(95,3),(96,3),(99,3),(102,3),(103,3),(104,3),(108,3),(109,3),(110,3),(111,3),(113,3),(115,3),(116,3),(117,3),(119,3),(120,3),(121,3),(125,3),(127,3),(130,3),(133,3),(136,3),(137,3),(138,3),(139,3),(140,3),(143,3),(145,3),(147,3),(148,3),(149,3),(150,3),(151,3),(152,3),(153,3),(154,3),(158,3),(159,3),(162,3),(165,3),(167,3),(170,3),(172,3),(173,3),(174,3),(175,3),(178,3),(179,3),(180,3),(184,3),(186,3),(189,3),(196,3),(198,3),(200,3),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(10,4),(11,4),(12,4),(13,4),(17,4),(19,4),(21,4),(22,4),(23,4),(27,4),(30,4),(31,4),(32,4),(34,4),(37,4),(38,4),(40,4),(42,4),(44,4),(51,4),(52,4),(54,4),(57,4),(58,4),(60,4),(61,4),(62,4),(64,4),(65,4),(68,4),(69,4),(70,4),(72,4),(74,4),(76,4),(77,4),(78,4),(81,4),(84,4),(86,4),(87,4),(91,4),(93,4),(94,4),(97,4),(98,4),(99,4),(101,4),(102,4),(105,4),(106,4),(109,4),(110,4),(111,4),(112,4),(114,4),(116,4),(117,4),(118,4),(122,4),(123,4),(124,4),(125,4),(126,4),(129,4),(131,4),(132,4),(133,4),(136,4),(138,4),(139,4),(141,4),(142,4),(143,4),(144,4),(146,4),(147,4),(151,4),(152,4),(153,4),(155,4),(156,4),(157,4),(162,4),(163,4),(164,4),(166,4),(173,4),(174,4),(175,4),(180,4),(181,4),(182,4),(183,4),(184,4),(186,4),(187,4),(188,4),(189,4),(190,4),(191,4),(192,4),(193,4),(194,4),(195,4),(196,4),(197,4),(198,4),(199,4);
/*!40000 ALTER TABLE `user_focus_area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'resalerealestatedb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-22 18:49:50
