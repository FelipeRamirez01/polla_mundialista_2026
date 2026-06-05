-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: polla_mundial
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `escenarios_terceros_fifa`
--

use railway;

DROP TABLE IF EXISTS `escenarios_terceros_fifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escenarios_terceros_fifa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `combinacion` varchar(50) NOT NULL,
  `posicion` varchar(20) NOT NULL,
  `grupo_tercero` char(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `escenarios_terceros_fifa`
--

LOCK TABLES `escenarios_terceros_fifa` WRITE;
/*!40000 ALTER TABLE `escenarios_terceros_fifa` DISABLE KEYS */;
/*!40000 ALTER TABLE `escenarios_terceros_fifa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos`
--

DROP TABLE IF EXISTS `grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
INSERT INTO `grupos` VALUES (1,'Amigos Mundial','MUNDIAL2026');
/*!40000 ALTER TABLE `grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `llaves_fifa_2026`
--

DROP TABLE IF EXISTS `llaves_fifa_2026`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `llaves_fifa_2026` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ronda` varchar(50) NOT NULL,
  `numero_partido` int NOT NULL,
  `posicion_local` varchar(20) NOT NULL,
  `posicion_visitante` varchar(20) NOT NULL,
  `siguiente_partido` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `llaves_fifa_2026`
--

LOCK TABLES `llaves_fifa_2026` WRITE;
/*!40000 ALTER TABLE `llaves_fifa_2026` DISABLE KEYS */;
/*!40000 ALTER TABLE `llaves_fifa_2026` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partidos`
--

DROP TABLE IF EXISTS `partidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fase` varchar(50) DEFAULT NULL,
  `grupo` varchar(5) DEFAULT NULL,
  `numero_partido` int DEFAULT NULL,
  `equipo_local` varchar(100) DEFAULT NULL,
  `equipo_visitante` varchar(100) DEFAULT NULL,
  `goles_local` int DEFAULT NULL,
  `goles_visitante` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `finalizado` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=281 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partidos`
--

LOCK TABLES `partidos` WRITE;
/*!40000 ALTER TABLE `partidos` DISABLE KEYS */;
INSERT INTO `partidos` VALUES (1,'Grupos','A',1,'Mexico','Sudafrica',NULL,NULL,'2026-06-11 14:00:00',0),(2,'Grupos','A',2,'Corea del Sur','Republica Checa',NULL,NULL,'2026-06-11 21:00:00',0),(3,'Grupos','A',3,'Republica Checa','Sudafrica',NULL,NULL,'2026-06-18 11:00:00',0),(4,'Grupos','A',4,'Mexico','Corea del Sur',NULL,NULL,'2026-06-18 20:00:00',0),(5,'Grupos','A',5,'Republica Checa','Mexico',NULL,NULL,'2026-06-24 20:00:00',0),(6,'Grupos','A',6,'Sudafrica','Corea del Sur',NULL,NULL,'2026-06-24 20:00:00',0),(7,'Grupos','B',7,'Canada','Bosnia Y Herzegovina',NULL,NULL,'2026-06-12 14:00:00',0),(8,'Grupos','B',8,'Catar','Suiza',NULL,NULL,'2026-06-13 00:00:00',0),(9,'Grupos','B',9,'Suiza','Bosnia Y Herzegovina',NULL,NULL,'2026-06-18 00:00:00',0),(10,'Grupos','B',10,'Canada','Catar',NULL,NULL,'2026-06-18 00:00:00',0),(11,'Grupos','B',11,'Suiza','Canada',NULL,NULL,'2026-06-24 00:00:00',0),(12,'Grupos','B',12,'Bosnia Y Herzegovina','Catar',NULL,NULL,'2026-06-24 00:00:00',0),(13,'Grupos','C',13,'Brasil','Marruecos',NULL,NULL,'2026-06-13 00:00:00',0),(14,'Grupos','C',14,'Haiti','Escocia',NULL,NULL,'2026-06-13 00:00:00',0),(15,'Grupos','C',15,'Brasil','Haiti',NULL,NULL,'2026-06-19 00:00:00',0),(16,'Grupos','C',16,'Escocia','Marruecos',NULL,NULL,'2026-06-19 00:00:00',0),(17,'Grupos','C',17,'Escocia','Brasil',NULL,NULL,'2026-06-24 00:00:00',0),(18,'Grupos','C',18,'Marruecos','Haiti',NULL,NULL,'2026-06-24 00:00:00',0),(19,'Grupos','D',19,'Estados Unidos','Paraguay',NULL,NULL,'2026-06-12 00:00:00',0),(20,'Grupos','D',20,'Australia','Turquia',NULL,NULL,'2026-06-13 00:00:00',0),(21,'Grupos','D',21,'Turquia','Paraguay',NULL,NULL,'2026-06-19 00:00:00',0),(22,'Grupos','D',22,'Estados Unidos','Australia',NULL,NULL,'2026-06-19 00:00:00',0),(23,'Grupos','D',23,'Turquia','Estados Unidos',NULL,NULL,'2026-06-25 00:00:00',0),(24,'Grupos','D',24,'Paraguay','Australia',NULL,NULL,'2026-06-25 00:00:00',0),(25,'Grupos','E',25,'Alemania','Curazao',NULL,NULL,'2026-06-14 00:00:00',0),(26,'Grupos','E',26,'Costa de Marfil','Ecuador',NULL,NULL,'2026-06-14 00:00:00',0),(27,'Grupos','E',27,'Alemania','Costa de Marfil',NULL,NULL,'2026-06-20 00:00:00',0),(28,'Grupos','E',28,'Ecuador','Curazao',NULL,NULL,'2026-06-20 00:00:00',0),(29,'Grupos','E',29,'Ecuador','Alemania',NULL,NULL,'2026-06-25 00:00:00',0),(30,'Grupos','E',30,'Curazao','Costa de Marfil',NULL,NULL,'2026-06-25 00:00:00',0),(31,'Grupos','F',31,'Paises Bajos','Japon',NULL,NULL,'2026-06-14 00:00:00',0),(32,'Grupos','F',32,'Suecia','Tunez',NULL,NULL,'2026-06-14 00:00:00',0),(33,'Grupos','F',33,'Paises Bajos','Suecia',NULL,NULL,'2026-06-20 00:00:00',0),(34,'Grupos','F',34,'Tunez','Japon',NULL,NULL,'2026-06-20 00:00:00',0),(35,'Grupos','F',35,'Japon','Suecia',NULL,NULL,'2026-06-25 00:00:00',0),(36,'Grupos','F',36,'Tunez','Paises Bajos',NULL,NULL,'2026-06-25 00:00:00',0),(37,'Grupos','G',37,'Iran','Nueva Zelanda',NULL,NULL,'2026-06-15 00:00:00',0),(38,'Grupos','G',38,'Belgica','Egipto',NULL,NULL,'2026-06-15 00:00:00',0),(39,'Grupos','G',39,'Belgica','Iran',NULL,NULL,'2026-06-21 00:00:00',0),(40,'Grupos','G',40,'Nueva Zelanda','Egipto',NULL,NULL,'2026-06-21 00:00:00',0),(41,'Grupos','G',41,'Nueva Zelanda','Belgica',NULL,NULL,'2026-06-26 00:00:00',0),(42,'Grupos','G',42,'Egipto','Iran',NULL,NULL,'2026-06-26 00:00:00',0),(43,'Grupos','H',43,'España','Cabo Verde',NULL,NULL,'2026-06-15 00:00:00',0),(44,'Grupos','H',44,'Arabia Saudita','Uruguay',NULL,NULL,'2026-06-15 00:00:00',0),(45,'Grupos','H',45,'España','Arabia Saudita',NULL,NULL,'2026-06-21 00:00:00',0),(46,'Grupos','H',46,'Uruguay','Cabo Verde',NULL,NULL,'2026-06-21 00:00:00',0),(47,'Grupos','H',47,'Uruguay','España',NULL,NULL,'2026-06-26 00:00:00',0),(48,'Grupos','H',48,'Cabo Verde','Arabia Saudita',NULL,NULL,'2026-06-26 00:00:00',0),(49,'Grupos','I',49,'Francia','Senegal',NULL,NULL,'2026-06-16 00:00:00',0),(50,'Grupos','I',50,'Irak','Noruega',NULL,NULL,'2026-06-16 00:00:00',0),(51,'Grupos','I',51,'Francia','Irak',NULL,NULL,'2026-06-22 00:00:00',0),(52,'Grupos','I',52,'Noruega','Senegal',NULL,NULL,'2026-06-22 00:00:00',0),(53,'Grupos','I',53,'Noruega','Francia',NULL,NULL,'2026-06-26 00:00:00',0),(54,'Grupos','I',54,'Senegal','Irak',NULL,NULL,'2026-06-26 00:00:00',0),(55,'Grupos','J',55,'Argentina','Argelia',NULL,NULL,'2026-06-16 00:00:00',0),(56,'Grupos','J',56,'Austria','Jordania',NULL,NULL,'2026-06-16 00:00:00',0),(57,'Grupos','J',57,'Argentina','Austria',NULL,NULL,'2026-06-22 00:00:00',0),(58,'Grupos','J',58,'Jordania','Argelia',NULL,NULL,'2026-06-22 00:00:00',0),(59,'Grupos','J',59,'Jordania','Argentina',NULL,NULL,'2026-06-27 00:00:00',0),(60,'Grupos','J',60,'Argelia','Austria',NULL,NULL,'2026-06-27 00:00:00',0),(61,'Grupos','K',61,'Portugal','Republica Democratica del Congo',NULL,NULL,'2026-06-17 00:00:00',0),(62,'Grupos','K',62,'Uzbekistan','Colombia',NULL,NULL,'2026-06-17 00:00:00',0),(63,'Grupos','K',63,'Portugal','Uzbekistan',NULL,NULL,'2026-06-23 00:00:00',0),(64,'Grupos','K',64,'Colombia','Republica Democratica del Congo',NULL,NULL,'2026-06-23 00:00:00',0),(65,'Grupos','K',65,'Colombia','Portugal',NULL,NULL,'2026-06-27 00:00:00',0),(66,'Grupos','K',66,'Republica Democratica del Congo','Uzbekistan',NULL,NULL,'2026-06-27 00:00:00',0),(67,'Grupos','L',67,'Inglaterra','Croacia',NULL,NULL,'2026-06-17 00:00:00',0),(68,'Grupos','L',68,'Ghana','Panama',NULL,NULL,'2026-06-17 00:00:00',0),(69,'Grupos','L',69,'Inglaterra','Ghana',NULL,NULL,'2026-06-23 00:00:00',0),(70,'Grupos','L',70,'Panama','Croacia',NULL,NULL,'2026-06-23 00:00:00',0),(71,'Grupos','L',71,'Panama','Inglaterra',NULL,NULL,'2026-06-27 00:00:00',0),(72,'Grupos','L',72,'Croacia','Ghana',NULL,NULL,'2026-06-27 00:00:00',0),(73,'Dieciseisavos','',73,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(74,'Dieciseisavos','',74,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(75,'Dieciseisavos','',75,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(76,'Dieciseisavos','',76,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(77,'Dieciseisavos','',77,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(78,'Dieciseisavos','',78,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(79,'Dieciseisavos','',79,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(80,'Dieciseisavos','',80,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(81,'Dieciseisavos','',81,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(82,'Dieciseisavos','',82,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(83,'Dieciseisavos','',83,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(84,'Dieciseisavos','',84,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(85,'Dieciseisavos','',85,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(86,'Dieciseisavos','',86,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(87,'Dieciseisavos','',87,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(88,'Dieciseisavos','',88,'Por definir','Por definir',NULL,NULL,'2026-07-01 00:00:00',0),(89,'Octavos','',89,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(90,'Octavos','',90,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(91,'Octavos','',91,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(92,'Octavos','',92,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(93,'Octavos','',93,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(94,'Octavos','',94,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(95,'Octavos','',95,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(96,'Octavos','',96,'Por definir','Por definir',NULL,NULL,'2026-07-05 00:00:00',0),(97,'Cuartos','',97,'Por definir','Por definir',NULL,NULL,'2026-07-09 00:00:00',0),(98,'Cuartos','',98,'Por definir','Por definir',NULL,NULL,'2026-07-09 00:00:00',0),(99,'Cuartos','',99,'Por definir','Por definir',NULL,NULL,'2026-07-09 00:00:00',0),(100,'Cuartos','',100,'Por definir','Por definir',NULL,NULL,'2026-07-09 00:00:00',0),(101,'Semifinal','',101,'Por definir','Por definir',NULL,NULL,'2026-07-13 00:00:00',0),(102,'Semifinal','',102,'Por definir','Por definir',NULL,NULL,'2026-07-13 00:00:00',0),(103,'Tercer Puesto','',103,'Por definir','Por definir',NULL,NULL,'2026-07-18 00:00:00',0),(104,'Final','',104,'Por definir','Por definir',NULL,NULL,'2026-07-19 00:00:00',0);
/*!40000 ALTER TABLE `partidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partidos_eliminacion`
--

DROP TABLE IF EXISTS `partidos_eliminacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partidos_eliminacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fase` enum('Dieciseisavos','Octavos','Cuartos','Semifinal','Tercer Puesto','Final') NOT NULL,
  `numero_partido` int NOT NULL,
  `equipo_local` varchar(100) NOT NULL,
  `equipo_visitante` varchar(100) NOT NULL,
  `goles_local` int DEFAULT NULL,
  `goles_visitante` int DEFAULT NULL,
  `ganador` varchar(100) DEFAULT NULL,
  `perdedor` varchar(100) DEFAULT NULL,
  `partido_origen_local` int DEFAULT NULL,
  `partido_origen_visitante` int DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `es_oficial` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`,`numero_partido`),
  CONSTRAINT `fk_pe_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partidos_eliminacion`
--

LOCK TABLES `partidos_eliminacion` WRITE;
/*!40000 ALTER TABLE `partidos_eliminacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `partidos_eliminacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `predicciones`
--

DROP TABLE IF EXISTS `predicciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `predicciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `partido_id` int DEFAULT NULL,
  `goles_local` int DEFAULT NULL,
  `goles_visitante` int DEFAULT NULL,
  `ganador` int DEFAULT NULL,
  `puntos` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `partido_id` (`partido_id`),
  CONSTRAINT `predicciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `predicciones_ibfk_2` FOREIGN KEY (`partido_id`) REFERENCES `partidos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predicciones`
--

LOCK TABLES `predicciones` WRITE;
/*!40000 ALTER TABLE `predicciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `predicciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador'),(2,'Usuario');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabla_posiciones`
--

DROP TABLE IF EXISTS `tabla_posiciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tabla_posiciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `grupo_id` int NOT NULL,
  `puntos` int DEFAULT NULL,
  `partidos_acertados` int DEFAULT NULL,
  `marcadores_exactos` int DEFAULT NULL,
  `posicion` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `grupo_id` (`grupo_id`),
  CONSTRAINT `tabla_posiciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `tabla_posiciones_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabla_posiciones`
--

LOCK TABLES `tabla_posiciones` WRITE;
/*!40000 ALTER TABLE `tabla_posiciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `tabla_posiciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol_id` int DEFAULT NULL,
  `grupo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  KEY `rol_id` (`rol_id`),
  KEY `grupo_id` (`grupo_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Administrador General','admin@admin.com','scrypt:32768:8:1$ubBMJeCRA8j9MxaU$ace85517dd02ab0855c3e29bf9189359a781833f6e7d2a438a7b5349c25474ee08552e56ed5dc2cfdccd772c68bf13e2621263481b0a316bd027c5b64be85c43',1,NULL),(2,'Usuario','usuario@usuario.com','scrypt:32768:8:1$ubBMJeCRA8j9MxaU$ace85517dd02ab0855c3e29bf9189359a781833f6e7d2a438a7b5349c25474ee08552e56ed5dc2cfdccd772c68bf13e2621263481b0a316bd027c5b64be85c43',2,1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-05 16:11:40
