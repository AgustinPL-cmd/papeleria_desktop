CREATE DATABASE papeleria_gomi;
USE papeleria_gomi;

-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: papeleria_marlons
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `alertasinventario`
--

DROP TABLE IF EXISTS `alertasinventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alertasinventario` (
  `id_alerta` int NOT NULL AUTO_INCREMENT,
  `fecha_alerta` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('pendiente','resuelto') DEFAULT 'pendiente',
  `productoId` int NOT NULL,
  PRIMARY KEY (`id_alerta`),
  KEY `productoId` (`productoId`),
  CONSTRAINT `alertasinventario_ibfk_1` FOREIGN KEY (`productoId`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertasinventario`
--

LOCK TABLES `alertasinventario` WRITE;
/*!40000 ALTER TABLE `alertasinventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `alertasinventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(100) NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Papelería'),(2,'Material de Oficina'),(3,'Arte y Dibujo'),(4,'Escolar'),(5,'Electrónica'),(6,'Papelería'),(7,'Material de Oficina'),(8,'Arte y Dibujo'),(9,'Escolar'),(10,'Electrónica');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion` text,
  `precio_unitario_venta` decimal(10,2) NOT NULL,
  `precio_unitario_compra` decimal(10,2) NOT NULL,
  `stock_actual` int NOT NULL,
  `stock_minimo` int NOT NULL,
  `id_categoria` int DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `id_categoria` (`id_categoria`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Lápiz HB','Lápiz grafito número 2',5.00,2.50,88,20,1),(2,'Cuaderno Profesional','Cuaderno de 100 hojas rayadas',45.00,25.00,42,10,4),(3,'Bolígrafo Azul','Paquete con 10 bolígrafos azules',35.00,18.00,74,15,1),(4,'Tijeras Escolares','Tijeras de punta redonda',25.00,12.00,24,5,4),(5,'Goma de Borrar','Goma blanca estándar',8.00,3.50,104,30,1),(6,'Marcadores Permanentes','Set de 6 colores',65.00,35.00,37,8,3),(7,'Calculadora Científica','Calculadora con 240 funciones',150.00,90.00,10,3,5),(8,'Carpeta de Argollas','Carpeta tamaño carta con argollas',55.00,30.00,20,5,2),(9,'Resaltadores','Paquete con 5 colores',40.00,22.00,52,12,1),(10,'USB 32GB','Memoria USB marca Kingston',120.00,70.00,17,4,5),(11,'Lápiz HB','Lápiz grafito número 2',5.00,2.50,100,20,1),(12,'Cuaderno Profesional','Cuaderno de 100 hojas rayadas',45.00,25.00,50,10,4),(13,'Bolígrafo Azul','Paquete con 10 bolígrafos azules',35.00,18.00,80,15,1),(14,'Tijeras Escolares','Tijeras de punta redonda',25.00,12.00,30,5,4),(15,'Goma de Borrar','Goma blanca estándar',8.00,3.50,120,30,1),(16,'Marcadores Permanentes','Set de 6 colores',65.00,35.00,40,8,3),(17,'Calculadora Científica','Calculadora con 240 funciones',150.00,90.00,15,3,5),(18,'Carpeta de Argollas','Carpeta tamaño carta con argollas',55.00,30.00,25,5,2),(19,'Resaltadores','Paquete con 5 colores',40.00,22.00,60,12,1),(20,'USB 32GB','Memoria USB marca Kingston',120.00,70.00,20,4,5),(21,'Nuevo producto Web','Prueba de producto',15.00,10.00,50,5,5);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/  /*!50003 TRIGGER `ValidarPrecioVentaVsCosto` BEFORE INSERT ON `productos` FOR EACH ROW BEGIN
    IF NEW.precio_unitario_venta < NEW.precio_unitario_compra THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR: El precio de venta no puede ser menor que el costo de compra';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `sugerenciasclientes`
--

DROP TABLE IF EXISTS `sugerenciasclientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sugerenciasclientes` (
  `id_sugerencia` int NOT NULL AUTO_INCREMENT,
  `fecha_sugerencia` datetime DEFAULT CURRENT_TIMESTAMP,
  `producto_sugerido` varchar(100) DEFAULT NULL,
  `comentario` text,
  PRIMARY KEY (`id_sugerencia`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sugerenciasclientes`
--

LOCK TABLES `sugerenciasclientes` WRITE;
/*!40000 ALTER TABLE `sugerenciasclientes` DISABLE KEYS */;
INSERT INTO `sugerenciasclientes` VALUES (1,'2025-06-18 07:06:01','Fomi moldeable','Agregar fomi moldeable de colores'),(3,'2026-03-01 19:07:46','Sugerencia de prueba1','Prueba1');
/*!40000 ALTER TABLE `sugerenciasclientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` enum('encargado','empleado') NOT NULL,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','admin123','encargado',1),(2,'Juan Pérez','emp123','empleado',1),(3,'Ana López','emp456','empleado',1),(4,'Agustín','agus123','empleado',1),(5,'empleadotest','123','empleado',1),(6,'admin','admin123','encargado',1),(7,'Juan Pérez','emp123','empleado',1),(8,'Ana López','emp456','empleado',1),(9,'EmpleadoWeb','web123','empleado',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `fecha_venta` datetime DEFAULT CURRENT_TIMESTAMP,
  `cantidad` int NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `numVenta` int NOT NULL,
  `productoId` int NOT NULL,
  `usuarioId` int NOT NULL,
  PRIMARY KEY (`id_venta`),
  KEY `usuarioId` (`usuarioId`),
  KEY `productoId` (`productoId`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`usuarioId`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`productoId`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,'2025-06-18 07:01:38',2,10.00,1001,1,2),(2,'2025-06-18 07:01:38',1,45.00,1001,2,2),(3,'2025-06-18 07:01:38',3,75.00,1002,3,2),(4,'2025-06-18 07:01:38',1,25.00,1002,4,2),(5,'2025-06-18 07:01:38',2,16.00,1003,5,2),(6,'2025-06-18 07:01:38',1,65.00,1003,6,2),(7,'2025-06-18 07:01:38',1,150.00,1004,7,2),(8,'2025-06-18 07:01:38',2,110.00,1004,8,2),(9,'2025-06-18 07:01:38',3,120.00,1005,9,2),(10,'2025-06-18 07:01:38',1,120.00,1005,10,2),(11,'2025-06-17 07:01:38',5,25.00,1006,1,2),(12,'2025-06-17 07:01:38',2,90.00,1006,2,2),(13,'2025-06-17 07:01:38',1,35.00,1007,3,2),(14,'2025-06-17 07:01:38',3,75.00,1007,4,2),(15,'2025-06-17 07:01:38',4,32.00,1008,5,2),(16,'2025-06-17 07:01:38',1,65.00,1008,6,2),(17,'2025-06-17 07:01:38',2,300.00,1009,7,2),(18,'2025-06-17 07:01:38',1,55.00,1009,8,2),(19,'2025-06-17 07:01:38',2,80.00,1010,9,2),(20,'2025-06-17 07:01:38',1,120.00,1010,10,2),(21,'2025-06-16 07:01:38',3,15.00,1011,1,2),(22,'2025-06-16 07:01:38',1,45.00,1011,2,2),(23,'2025-06-15 07:01:38',2,70.00,1012,3,2),(24,'2025-06-15 07:01:38',1,25.00,1012,4,2),(25,'2025-06-14 07:01:38',5,40.00,1013,5,2),(26,'2025-06-14 07:01:38',1,65.00,1013,6,2),(27,'2025-06-13 07:01:38',1,150.00,1014,7,2),(28,'2025-06-13 07:01:38',2,110.00,1014,8,2),(29,'2025-06-12 07:01:38',3,120.00,1015,9,2),(30,'2025-06-12 07:01:38',1,120.00,1015,10,2),(31,'2025-06-18 07:01:38',3,15.00,1016,1,3),(32,'2025-06-18 07:01:38',1,45.00,1016,2,3),(33,'2025-06-18 07:01:38',2,70.00,1017,3,3),(34,'2025-06-18 07:01:38',1,25.00,1017,4,3),(35,'2025-06-18 07:01:38',4,32.00,1018,5,3),(36,'2025-06-18 07:01:38',1,65.00,1018,6,3),(37,'2025-06-18 07:01:38',1,150.00,1019,7,3),(38,'2025-06-18 07:01:38',2,110.00,1019,8,3),(39,'2025-06-18 07:01:38',3,120.00,1020,9,3),(40,'2025-06-18 07:01:38',1,120.00,1020,10,3),(41,'2025-06-18 00:00:00',2,10.00,1021,1,2),(42,'2025-06-18 00:00:00',1,25.00,1021,4,2),(43,'2025-06-18 00:00:00',2,10.00,1022,1,2),(44,'2025-06-18 00:00:00',2,90.00,1022,2,2),(45,'2025-06-18 00:00:00',3,15.00,1023,1,2),(46,'2025-06-18 00:00:00',2,90.00,1023,2,2),(47,'2025-07-01 19:48:35',2,10.00,1001,1,2),(48,'2025-07-01 19:48:35',1,45.00,1001,2,2),(49,'2025-07-01 19:48:35',3,75.00,1002,3,2),(50,'2025-07-01 19:48:35',1,25.00,1002,4,2),(51,'2025-07-01 19:48:35',2,16.00,1003,5,2),(52,'2025-07-01 19:48:35',1,65.00,1003,6,2),(53,'2025-07-01 19:48:35',1,150.00,1004,7,2),(54,'2025-07-01 19:48:35',2,110.00,1004,8,2),(55,'2025-07-01 19:48:35',3,120.00,1005,9,2),(56,'2025-07-01 19:48:35',1,120.00,1005,10,2),(57,'2025-06-30 19:48:35',5,25.00,1006,1,2),(58,'2025-06-30 19:48:35',2,90.00,1006,2,2),(59,'2025-06-30 19:48:35',1,35.00,1007,3,2),(60,'2025-06-30 19:48:35',3,75.00,1007,4,2),(61,'2025-06-30 19:48:35',4,32.00,1008,5,2),(62,'2025-06-30 19:48:35',1,65.00,1008,6,2),(63,'2025-06-30 19:48:35',2,300.00,1009,7,2),(64,'2025-06-30 19:48:35',1,55.00,1009,8,2),(65,'2025-06-30 19:48:35',2,80.00,1010,9,2),(66,'2025-06-30 19:48:35',1,120.00,1010,10,2),(67,'2025-06-29 19:48:35',3,15.00,1011,1,2),(68,'2025-06-29 19:48:35',1,45.00,1011,2,2),(69,'2025-06-28 19:48:35',2,70.00,1012,3,2),(70,'2025-06-28 19:48:35',1,25.00,1012,4,2),(71,'2025-06-27 19:48:35',5,40.00,1013,5,2),(72,'2025-06-27 19:48:35',1,65.00,1013,6,2),(73,'2025-06-26 19:48:35',1,150.00,1014,7,2),(74,'2025-06-26 19:48:35',2,110.00,1014,8,2),(75,'2025-06-25 19:48:35',3,120.00,1015,9,2),(76,'2025-06-25 19:48:35',1,120.00,1015,10,2),(77,'2026-03-01 00:00:00',1,5.00,1024,1,2),(78,'2026-03-01 00:00:00',1,150.00,1024,7,2),(79,'2026-03-01 00:00:00',5,40.00,1025,5,2),(80,'2026-03-01 00:00:00',1,5.00,1025,1,2);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/  /*!50003 TRIGGER `tr_reducir_stock_venta` AFTER INSERT ON `ventas` FOR EACH ROW BEGIN
    UPDATE productos
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id_producto = NEW.productoId;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping events for database 'papeleria_marlons'
--

--
-- Dumping routines for database 'papeleria_marlons'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-02 11:51:07
