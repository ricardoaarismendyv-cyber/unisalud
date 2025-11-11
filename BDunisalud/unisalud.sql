-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: unisaludbd
-- ------------------------------------------------------
-- Server version	9.5.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

-- SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '74c21445-bcd3-11f0-960a-00e04c062625:1-437';

--
-- Table structure for table `afiliacion`
--

DROP TABLE IF EXISTS `afiliacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `afiliacion` (
  `id_afiliacion` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_paciente` int NOT NULL COMMENT 'Referencia a PACIENTES',
  `id_eps` int NOT NULL COMMENT 'Referencia a EPS',
  `id_tipo_afiliacion` int NOT NULL COMMENT 'Referencia a TIPOS_AFILIACION',
  `fecha_inicio` date NOT NULL COMMENT 'Fecha de inicio afliacion',
  `fecha_fin` date DEFAULT NULL COMMENT 'Fecha de fin de la afiliacion',
  `estado_afiliacion` enum('Activa','Inactiva','Suspendida') DEFAULT 'Activa' COMMENT 'Esta: activo, inactivo',
  PRIMARY KEY (`id_afiliacion`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_eps` (`id_eps`),
  KEY `id_tipo_afiliacion` (`id_tipo_afiliacion`),
  CONSTRAINT `afiliacion_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `afiliacion_ibfk_2` FOREIGN KEY (`id_eps`) REFERENCES `eps` (`id_eps`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `afiliacion_ibfk_3` FOREIGN KEY (`id_tipo_afiliacion`) REFERENCES `tipos_afiliacion` (`id_tipo_afiliacion`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_fechas` CHECK (((`fecha_fin` is null) or (`fecha_fin` >= `fecha_inicio`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `afiliacion`
--

LOCK TABLES `afiliacion` WRITE;
/*!40000 ALTER TABLE `afiliacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `afiliacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `antecedentes_paciente`
--

DROP TABLE IF EXISTS `antecedentes_paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `antecedentes_paciente` (
  `id_antecedente` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_paciente` int NOT NULL COMMENT 'Referencia a PACIENTES',
  `tipo_antecedente` enum('Familiar','Personal','Quirurgico','Traumatico','Alergias','Farmacologico') NOT NULL COMMENT 'si es: familiar, personal, etc',
  `descripcion` text NOT NULL COMMENT 'Descripcion',
  `fecha_registro` date DEFAULT NULL COMMENT 'Fecha de registro',
  `severidad` enum('Leve','Moderada','Grave','Critica') DEFAULT NULL COMMENT 'es: leve, moderada, etc',
  `estado_antecedente` enum('Activo','Resuelto','En Observacion') DEFAULT 'Activo' COMMENT 'Esta: activo, resuelto, etc',
  PRIMARY KEY (`id_antecedente`),
  KEY `id_paciente` (`id_paciente`),
  CONSTRAINT `antecedentes_paciente_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `antecedentes_paciente`
--

LOCK TABLES `antecedentes_paciente` WRITE;
/*!40000 ALTER TABLE `antecedentes_paciente` DISABLE KEYS */;
/*!40000 ALTER TABLE `antecedentes_paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `centros_medicos`
--

DROP TABLE IF EXISTS `centros_medicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `centros_medicos` (
  `id_centro_medico` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_centro` varchar(150) NOT NULL COMMENT 'Nombre del centro medico',
  `id_red_salud` int DEFAULT NULL COMMENT 'Referencia a REDES_SALUD',
  `id_nivel_atencion` int NOT NULL COMMENT 'Referencia a NIVELES_ATENCION',
  `id_ciudad` int NOT NULL COMMENT 'Referencia a CIUDAD',
  `direccion` varchar(255) NOT NULL COMMENT 'Direccion centro medico',
  `latitud` decimal(10,8) DEFAULT NULL COMMENT 'Latitud, localizacion geografica',
  `longitud` decimal(10,8) DEFAULT NULL COMMENT 'Longitud, localizacion geografica',
  `telefono` varchar(15) DEFAULT NULL COMMENT 'Telefono centro medico',
  `celular` varchar(15) DEFAULT NULL COMMENT 'Celular centro medico',
  `correo` varchar(100) DEFAULT NULL COMMENT 'Correo entro medico',
  `sitio_web` varchar(150) DEFAULT NULL COMMENT 'Sitio web centro medico',
  `codigo_habilitacion` varchar(50) DEFAULT NULL COMMENT 'Codigo de habilitacion REPS',
  `fecha_habilitacion` date DEFAULT NULL COMMENT 'Fecha de habilitacion REPS',
  `estado_centro` enum('Activo','Inactivo','En Reforma') DEFAULT 'Activo' COMMENT 'Esta activa, inactiva',
  PRIMARY KEY (`id_centro_medico`),
  UNIQUE KEY `codigo_habilitacion` (`codigo_habilitacion`),
  KEY `id_red_salud` (`id_red_salud`),
  KEY `id_nivel_atencion` (`id_nivel_atencion`),
  KEY `id_ciudad` (`id_ciudad`),
  CONSTRAINT `centros_medicos_ibfk_1` FOREIGN KEY (`id_red_salud`) REFERENCES `redes_salud` (`id_red`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `centros_medicos_ibfk_2` FOREIGN KEY (`id_nivel_atencion`) REFERENCES `niveles_atencion` (`id_nivel`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `centros_medicos_ibfk_3` FOREIGN KEY (`id_ciudad`) REFERENCES `ciudad` (`id_ciudad`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `centros_medicos`
--

LOCK TABLES `centros_medicos` WRITE;
/*!40000 ALTER TABLE `centros_medicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `centros_medicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ciudad`
--

DROP TABLE IF EXISTS `ciudad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciudad` (
  `id_ciudad` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_ciudad` varchar(100) NOT NULL COMMENT 'Nombre de la ciudad',
  `id_departamento` int NOT NULL COMMENT 'Referencia a DEPARTAMENTO',
  `codigo_dane` varchar(10) DEFAULT NULL COMMENT 'Codigo DANE para identificar oficialmente c/ciudad',
  PRIMARY KEY (`id_ciudad`),
  KEY `id_departamento` (`id_departamento`),
  CONSTRAINT `ciudad_ibfk_1` FOREIGN KEY (`id_departamento`) REFERENCES `departamento` (`id_departamento`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciudad`
--

LOCK TABLES `ciudad` WRITE;
/*!40000 ALTER TABLE `ciudad` DISABLE KEYS */;
/*!40000 ALTER TABLE `ciudad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consulta`
--

DROP TABLE IF EXISTS `consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consulta` (
  `id_consulta` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_paciente` int NOT NULL COMMENT 'Referencia a PACIENTES',
  `id_profesional` int NOT NULL COMMENT 'Referencia a PROFESIONAL_SALUD',
  `id_centro_medico` int NOT NULL COMMENT 'Referencia a CENTROS_MEDICOS',
  `estado` enum('Programada','Atendida','Cancelada','No Asistio') DEFAULT 'Programada' COMMENT 'Esta: programada, atendido, etc',
  `fecha_programada` datetime NOT NULL COMMENT 'Fecha programada la consulta',
  `fecha_atencion` datetime DEFAULT NULL COMMENT 'Fecha de atencion consulta',
  `motivo_consulta` text COMMENT 'Motivo por la que el paciente asiste a la consulta',
  `anamnesis` text COMMENT 'informacion que aporta el paciente para crear el historial clinico',
  `examen_fisico` text COMMENT 'Examen fisico, exploratorio al paciente',
  `frecuencia_cardiaca` int DEFAULT NULL COMMENT 'FC en lpm',
  `frecuencia_respiratoria` int DEFAULT NULL COMMENT 'FR en rpm',
  `temperatura` decimal(4,2) DEFAULT NULL COMMENT 'Temperatura en °C',
  `saturacion_oxigeno` int DEFAULT NULL COMMENT 'SpO2 en %',
  `presion_arterial_sistolica` int DEFAULT NULL COMMENT 'TA sistolica',
  `presion_arterial_diastolica` int DEFAULT NULL COMMENT 'TA diastolica',
  `peso` decimal(5,2) DEFAULT NULL COMMENT 'Peso en kg',
  `talla` decimal(4,2) DEFAULT NULL COMMENT 'Talla en cm',
  `imc` decimal(4,2) DEFAULT NULL COMMENT 'Índice de Masa Corporal',
  `habitos_fumador` enum('Sí','No','Ocasional') DEFAULT NULL COMMENT '¿Fuma?',
  `habitos_alcohol` enum('Sí','No','Ocasional') DEFAULT NULL COMMENT '¿Consume alcohol?',
  `habitos_ejercicio` enum('Sí','No') DEFAULT NULL COMMENT '¿Realiza actividad fisica?',
  `revision_sistemas` text COMMENT 'Revision por sistemas',
  `impresion_diagnostica` text COMMENT 'Diagnostico al paciente',
  `plan_tratamiento` text COMMENT 'Plan de tratamiento para el paciente',
  `notas_adicionales` text COMMENT 'Notas del profesional salud, opcional',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro de la consulta',
  PRIMARY KEY (`id_consulta`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_profesional` (`id_profesional`),
  KEY `id_centro_medico` (`id_centro_medico`),
  CONSTRAINT `consulta_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`id_profesional`) REFERENCES `profesional_salud` (`id_profesional`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `consulta_ibfk_3` FOREIGN KEY (`id_centro_medico`) REFERENCES `centros_medicos` (`id_centro_medico`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consulta`
--

LOCK TABLES `consulta` WRITE;
/*!40000 ALTER TABLE `consulta` DISABLE KEYS */;
/*!40000 ALTER TABLE `consulta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamento`
--

DROP TABLE IF EXISTS `departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamento` (
  `id_departamento` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_departamento` varchar(100) NOT NULL COMMENT 'Nombre del departamento',
  `id_region` int DEFAULT NULL COMMENT 'Referencia a REGION_SALUD',
  `codigo_dane` varchar(10) DEFAULT NULL COMMENT 'Codigo DANE para identificar oficialmente c/depto.',
  PRIMARY KEY (`id_departamento`),
  KEY `id_region` (`id_region`),
  CONSTRAINT `departamento_ibfk_1` FOREIGN KEY (`id_region`) REFERENCES `region_salud` (`id_region`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamento`
--

LOCK TABLES `departamento` WRITE;
/*!40000 ALTER TABLE `departamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `departamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_medicamento`
--

DROP TABLE IF EXISTS `detalle_medicamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_medicamento` (
  `id_detalle` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_medicamento` int NOT NULL COMMENT 'Referencia al medicamento principal',
  `lote` varchar(50) NOT NULL COMMENT 'Numero de lote medicamento',
  `fecha_expiracion` date NOT NULL COMMENT 'Fecha de vencimiento medicamento',
  `condiciones_almacenamiento` text COMMENT 'Condiciones de almacenamiento medicamento',
  `cantidad_existente` int DEFAULT '0' COMMENT 'Cantidad disponible medicamento',
  `fecha_ingreso` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de ingreso medicamento',
  `estado` enum('Activo','Agotado','Retirado') DEFAULT 'Activo' COMMENT 'Estado del lote: activo, agotado, etc',
  PRIMARY KEY (`id_detalle`),
  UNIQUE KEY `uk_lote_medicamento` (`id_medicamento`,`lote`),
  CONSTRAINT `detalle_medicamento_ibfk_1` FOREIGN KEY (`id_medicamento`) REFERENCES `medicamentos` (`id_medicamento`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_medicamento`
--

LOCK TABLES `detalle_medicamento` WRITE;
/*!40000 ALTER TABLE `detalle_medicamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_medicamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diagnostico_paciente`
--

DROP TABLE IF EXISTS `diagnostico_paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diagnostico_paciente` (
  `id_diagnostico` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_consulta` int NOT NULL COMMENT 'Referencia a CONSULTA',
  `id_enfermedad` int NOT NULL COMMENT 'Referencia a ENFERMEDADES',
  `tipo_diagnostico` enum('Principal','Secundario','Presuntivo','Confirmado') DEFAULT 'Presuntivo' COMMENT 'Es: presuntivo, principal, etc',
  `notas` text COMMENT 'Notas',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro',
  PRIMARY KEY (`id_diagnostico`),
  KEY `id_consulta` (`id_consulta`),
  KEY `id_enfermedad` (`id_enfermedad`),
  CONSTRAINT `diagnostico_paciente_ibfk_1` FOREIGN KEY (`id_consulta`) REFERENCES `consulta` (`id_consulta`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `diagnostico_paciente_ibfk_2` FOREIGN KEY (`id_enfermedad`) REFERENCES `enfermedades` (`id_enfermedad`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diagnostico_paciente`
--

LOCK TABLES `diagnostico_paciente` WRITE;
/*!40000 ALTER TABLE `diagnostico_paciente` DISABLE KEYS */;
/*!40000 ALTER TABLE `diagnostico_paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enfermedades`
--

DROP TABLE IF EXISTS `enfermedades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enfermedades` (
  `id_enfermedad` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `codigo_cie10` varchar(10) NOT NULL COMMENT 'Codigo CIE-10 para clasificar diagnosticos, sintomas',
  `nombre_enfermedad` varchar(300) NOT NULL COMMENT 'Nombre de la enfermedad',
  `descripcion` text COMMENT 'Descripcion clinica de la enfermedad',
  `categoria` varchar(100) DEFAULT NULL COMMENT 'refiere si es aguda, cronica, infecciosa, etc',
  PRIMARY KEY (`id_enfermedad`),
  UNIQUE KEY `codigo_cie10` (`codigo_cie10`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enfermedades`
--

LOCK TABLES `enfermedades` WRITE;
/*!40000 ALTER TABLE `enfermedades` DISABLE KEYS */;
/*!40000 ALTER TABLE `enfermedades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eps`
--

DROP TABLE IF EXISTS `eps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eps` (
  `id_eps` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_eps` varchar(100) NOT NULL COMMENT 'Nombre de la EPS',
  `nit` varchar(20) DEFAULT NULL COMMENT 'NIT de la EPS',
  `direccion` varchar(255) DEFAULT NULL COMMENT 'Direccion de la EPS',
  `telefono` varchar(15) DEFAULT NULL COMMENT 'Telefono de la EPS',
  `correo` varchar(100) DEFAULT NULL COMMENT 'Correo de la EPS',
  `estado_eps` enum('Activa','Inactiva') DEFAULT 'Activa' COMMENT 'Esta activa, inactiva',
  PRIMARY KEY (`id_eps`),
  UNIQUE KEY `nombre_eps` (`nombre_eps`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eps`
--

LOCK TABLES `eps` WRITE;
/*!40000 ALTER TABLE `eps` DISABLE KEYS */;
/*!40000 ALTER TABLE `eps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especialidades`
--

DROP TABLE IF EXISTS `especialidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `especialidades` (
  `id_especialidad` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_especialidad` varchar(100) NOT NULL COMMENT 'refiere a la especialidad medica: neurologia, cardiologia, etc',
  `descripcion` text COMMENT 'Descripcion',
  `nivel_formacion` enum('Pregrado','Especializacion','Maestria','Subespecialidad') DEFAULT 'Especializacion' COMMENT 'Nivel de formacion',
  PRIMARY KEY (`id_especialidad`),
  UNIQUE KEY `nombre_especialidad` (`nombre_especialidad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especialidades`
--

LOCK TABLES `especialidades` WRITE;
/*!40000 ALTER TABLE `especialidades` DISABLE KEYS */;
/*!40000 ALTER TABLE `especialidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_civil`
--

DROP TABLE IF EXISTS `estado_civil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_civil` (
  `id_estado_civil` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_estado` varchar(20) NOT NULL COMMENT 'Ej: soltero, casado, etc',
  PRIMARY KEY (`id_estado_civil`),
  UNIQUE KEY `nombre_estado` (`nombre_estado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_civil`
--

LOCK TABLES `estado_civil` WRITE;
/*!40000 ALTER TABLE `estado_civil` DISABLE KEYS */;
/*!40000 ALTER TABLE `estado_civil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_orden`
--

DROP TABLE IF EXISTS `estado_orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_orden` (
  `id_estado_orden` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_estado_orden` varchar(20) NOT NULL COMMENT 'esta: pendiente, entregada, etc',
  PRIMARY KEY (`id_estado_orden`),
  UNIQUE KEY `nombre_estado_orden` (`nombre_estado_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_orden`
--

LOCK TABLES `estado_orden` WRITE;
/*!40000 ALTER TABLE `estado_orden` DISABLE KEYS */;
/*!40000 ALTER TABLE `estado_orden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estrato_socioeconomico`
--

DROP TABLE IF EXISTS `estrato_socioeconomico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estrato_socioeconomico` (
  `id_estrato` int NOT NULL COMMENT 'ID del 1 al 6',
  `descripcion` varchar(100) NOT NULL COMMENT 'Ej: Bajo, Medio, alto',
  PRIMARY KEY (`id_estrato`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estrato_socioeconomico`
--

LOCK TABLES `estrato_socioeconomico` WRITE;
/*!40000 ALTER TABLE `estrato_socioeconomico` DISABLE KEYS */;
/*!40000 ALTER TABLE `estrato_socioeconomico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genero`
--

DROP TABLE IF EXISTS `genero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genero` (
  `id_genero` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_genero` varchar(20) NOT NULL COMMENT 'Ej: Masculino, Femenino, No Binario, etc',
  PRIMARY KEY (`id_genero`),
  UNIQUE KEY `nombre_genero` (`nombre_genero`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genero`
--

LOCK TABLES `genero` WRITE;
/*!40000 ALTER TABLE `genero` DISABLE KEYS */;
/*!40000 ALTER TABLE `genero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupo_rh`
--

DROP TABLE IF EXISTS `grupo_rh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupo_rh` (
  `id_rh` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `tipo_rh` varchar(3) NOT NULL COMMENT 'Ej: A+, B-, etc',
  PRIMARY KEY (`id_rh`),
  UNIQUE KEY `tipo_rh` (`tipo_rh`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupo_rh`
--

LOCK TABLES `grupo_rh` WRITE;
/*!40000 ALTER TABLE `grupo_rh` DISABLE KEYS */;
/*!40000 ALTER TABLE `grupo_rh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incapacidad`
--

DROP TABLE IF EXISTS `incapacidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incapacidad` (
  `id_incapacidad` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_consulta` int NOT NULL COMMENT 'Consulta que genero la incapacidad',
  `id_paciente` int NOT NULL COMMENT 'Paciente al que se le emite la incapacidad',
  `id_profesional` int NOT NULL COMMENT 'Profesional que emite la incapacidad',
  `fecha_inicio` date NOT NULL COMMENT 'Fecha de inicio de la incapacidad',
  `fecha_fin` date NOT NULL COMMENT 'Fecha de fin de la incapacidad',
  `dias_incapacidad` int GENERATED ALWAYS AS (((to_days(`fecha_fin`) - to_days(`fecha_inicio`)) + 1)) STORED COMMENT 'Dias totales de la incapacidad',
  `motivo` text NOT NULL COMMENT 'Motivo de la incapacidad',
  `diagnostico_relacionado` text COMMENT 'Diagnostico que justifica la incapacidad',
  `observaciones` text COMMENT 'Notas adicionales',
  `estado` enum('Activa','Finalizada','Cancelada') DEFAULT 'Activa' COMMENT 'Esta: activa, finalizada, etc',
  `codigo_qr` varchar(255) DEFAULT NULL COMMENT 'Codigo QR para descarga de la incapacidad',
  `fecha_emision` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de emision incapacidad',
  PRIMARY KEY (`id_incapacidad`),
  KEY `id_consulta` (`id_consulta`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_profesional` (`id_profesional`),
  CONSTRAINT `incapacidad_ibfk_1` FOREIGN KEY (`id_consulta`) REFERENCES `consulta` (`id_consulta`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `incapacidad_ibfk_2` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `incapacidad_ibfk_3` FOREIGN KEY (`id_profesional`) REFERENCES `profesional_salud` (`id_profesional`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incapacidad`
--

LOCK TABLES `incapacidad` WRITE;
/*!40000 ALTER TABLE `incapacidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `incapacidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicamentos`
--

DROP TABLE IF EXISTS `medicamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicamentos` (
  `id_medicamento` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_comercial` varchar(200) NOT NULL COMMENT 'Nombre comercial medicamento',
  `nombre_generico` varchar(200) DEFAULT NULL COMMENT 'Nombre generico medicamento',
  `principio_activo` varchar(100) DEFAULT NULL COMMENT 'Principio activo medicamento',
  `concentracion` varchar(50) DEFAULT NULL COMMENT 'Concentracion medicamento',
  `forma_farmaceutica` varchar(50) DEFAULT NULL COMMENT 'Forma farmaceutica medicamento',
  `via_administracion` varchar(50) DEFAULT NULL COMMENT 'Via de administracion medicamento',
  `registro_invima` varchar(100) NOT NULL COMMENT 'Registro INVIMA del medicamento',
  `fabricante` varchar(150) DEFAULT NULL COMMENT 'Fabricante del medicamento',
  `estado_medicamento` enum('Activo','Agotado','Retirado','En Revisión') DEFAULT 'Activo' COMMENT 'Esta activo, retirado, etc',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro medicamento',
  PRIMARY KEY (`id_medicamento`),
  UNIQUE KEY `registro_invima` (`registro_invima`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicamentos`
--

LOCK TABLES `medicamentos` WRITE;
/*!40000 ALTER TABLE `medicamentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `medicamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles_atencion`
--

DROP TABLE IF EXISTS `niveles_atencion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles_atencion` (
  `id_nivel` int NOT NULL COMMENT 'ID del nivel (1 a 3)',
  `nombre_nivel` varchar(50) NOT NULL COMMENT 'de acuerdo al grado de complejidad en salud: primer nivel-atencion basica...',
  `descripcion` text COMMENT 'Descripcion',
  PRIMARY KEY (`id_nivel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles_atencion`
--

LOCK TABLES `niveles_atencion` WRITE;
/*!40000 ALTER TABLE `niveles_atencion` DISABLE KEYS */;
/*!40000 ALTER TABLE `niveles_atencion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orden_medica`
--

DROP TABLE IF EXISTS `orden_medica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orden_medica` (
  `id_orden` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_paciente` int NOT NULL COMMENT 'Referencia a PACIENTE',
  `id_profesional` int NOT NULL COMMENT 'Referencia a PROFESIONAL_SALUD',
  `id_tipo_orden` int NOT NULL COMMENT 'Referencia a TIPO_ORDEN',
  `id_detalle_medicamento` int DEFAULT NULL COMMENT 'Referencia a DETALLE_MEDICAMENTOS',
  `id_servicio` int DEFAULT NULL COMMENT 'Referencia a SERVICIOS',
  `dosis` varchar(100) DEFAULT NULL COMMENT 'Dosis del medicamento',
  `duracion_tratamiento` varchar(100) DEFAULT NULL COMMENT 'De acuerdo al diagnostico',
  `frecuencia` varchar(50) DEFAULT NULL COMMENT 'Frecuencia de acuerdo al diagnostico',
  `cantidad` int DEFAULT NULL COMMENT 'Cantidad de acuerdo al diagnostico',
  `indicaciones` text COMMENT 'Indicaciones tratamiento y/o procedimiento',
  `id_centro_medico` int NOT NULL COMMENT 'Centro medico donde se emite',
  `id_estado_orden` int NOT NULL DEFAULT '1' COMMENT 'Referencia a ESTADO_ORDEN',
  `fecha_emision` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de emision de la orden',
  `fecha_cumplimiento` datetime DEFAULT NULL COMMENT 'Fecha de cumplimiento, máximo 30 días',
  `codigo_qr` varchar(255) DEFAULT NULL COMMENT 'Código QR para descarga segura',
  `id_consulta` int DEFAULT NULL COMMENT 'Referencia opcional a CONSULTA',
  PRIMARY KEY (`id_orden`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_profesional` (`id_profesional`),
  KEY `id_tipo_orden` (`id_tipo_orden`),
  KEY `id_detalle_medicamento` (`id_detalle_medicamento`),
  KEY `id_servicio` (`id_servicio`),
  KEY `id_centro_medico` (`id_centro_medico`),
  KEY `id_estado_orden` (`id_estado_orden`),
  KEY `id_consulta` (`id_consulta`),
  CONSTRAINT `orden_medica_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_2` FOREIGN KEY (`id_profesional`) REFERENCES `profesional_salud` (`id_profesional`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_3` FOREIGN KEY (`id_tipo_orden`) REFERENCES `tipo_orden` (`id_tipo`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_4` FOREIGN KEY (`id_detalle_medicamento`) REFERENCES `detalle_medicamento` (`id_detalle`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_5` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_servicio`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_6` FOREIGN KEY (`id_centro_medico`) REFERENCES `centros_medicos` (`id_centro_medico`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_7` FOREIGN KEY (`id_estado_orden`) REFERENCES `estado_orden` (`id_estado_orden`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `orden_medica_ibfk_8` FOREIGN KEY (`id_consulta`) REFERENCES `consulta` (`id_consulta`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden_medica`
--

LOCK TABLES `orden_medica` WRITE;
/*!40000 ALTER TABLE `orden_medica` DISABLE KEYS */;
/*!40000 ALTER TABLE `orden_medica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes`
--

DROP TABLE IF EXISTS `pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes` (
  `id_paciente` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_usuario` int DEFAULT NULL COMMENT 'Referencia a la cuenta de USUARIOS',
  `id_tipo_identificacion` int NOT NULL COMMENT 'Referencia a TIPO_IDENTIFICACION',
  `numero_documento` varchar(20) NOT NULL COMMENT 'Numero del documento paciente',
  `nombre1` varchar(50) NOT NULL COMMENT 'Primer nombre paciente',
  `nombre2` varchar(50) DEFAULT NULL COMMENT 'Segundo nombre paciente, opcional',
  `apellido1` varchar(50) NOT NULL COMMENT 'Primer apellido paciente',
  `apellido2` varchar(50) DEFAULT NULL COMMENT 'Segundo apellido paciente, opcional',
  `id_genero` int NOT NULL COMMENT 'Referencia a GENERO',
  `id_rh` int DEFAULT NULL COMMENT 'Referencia a GRUPO_RH',
  `fecha_nacimiento` date NOT NULL COMMENT 'Fecha de nacimiento paciente',
  `id_estado_civil` int DEFAULT NULL COMMENT 'Referencia a ESTADO_CIVIL',
  `id_estrato` int DEFAULT NULL COMMENT 'Referencia a ESTRATO',
  `direccion` varchar(255) DEFAULT NULL COMMENT 'Direccion paciente',
  `celular` varchar(15) DEFAULT NULL COMMENT 'Celular paciente',
  `telefono` varchar(15) DEFAULT NULL COMMENT 'Telefono fijo paciente, opcional',
  `correo_electronico` varchar(100) DEFAULT NULL COMMENT 'Correo paciente, opcional',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro paciente',
  PRIMARY KEY (`id_paciente`),
  UNIQUE KEY `uk_identificacion` (`id_tipo_identificacion`,`numero_documento`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  KEY `id_genero` (`id_genero`),
  KEY `id_rh` (`id_rh`),
  KEY `id_estado_civil` (`id_estado_civil`),
  KEY `id_estrato` (`id_estrato`),
  CONSTRAINT `pacientes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `pacientes_ibfk_2` FOREIGN KEY (`id_tipo_identificacion`) REFERENCES `tipo_identificacion` (`id_tipo_identificacion`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `pacientes_ibfk_3` FOREIGN KEY (`id_genero`) REFERENCES `genero` (`id_genero`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `pacientes_ibfk_4` FOREIGN KEY (`id_rh`) REFERENCES `grupo_rh` (`id_rh`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `pacientes_ibfk_5` FOREIGN KEY (`id_estado_civil`) REFERENCES `estado_civil` (`id_estado_civil`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `pacientes_ibfk_6` FOREIGN KEY (`id_estrato`) REFERENCES `estrato_socioeconomico` (`id_estrato`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profesional_salud`
--

DROP TABLE IF EXISTS `profesional_salud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profesional_salud` (
  `id_profesional` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_usuario` int NOT NULL COMMENT 'Referencia a la cuenta de USUARIOS (Obligatorio para personal)',
  `id_tipo_identificacion` int NOT NULL COMMENT 'Referencia a TIPO_IDENTIFICACION',
  `numero_documento` varchar(20) NOT NULL COMMENT 'Numero del documento profesional salud',
  `nombre1` varchar(50) NOT NULL COMMENT 'Primer nombre profesional salud',
  `nombre2` varchar(50) DEFAULT NULL COMMENT 'Segundo nombre profesional salud',
  `apellido1` varchar(50) NOT NULL COMMENT 'Primer apellido profesional salud',
  `apellido2` varchar(50) DEFAULT NULL COMMENT 'Segundo apellido profesional salud',
  `id_genero` int NOT NULL COMMENT 'Referencia a GENERO',
  `fecha_nacimiento` date DEFAULT NULL COMMENT 'Fecha de nacimiento profesional salud',
  `telefono` varchar(15) DEFAULT NULL COMMENT 'Telefono profesional salud, opcional',
  `celular` varchar(15) DEFAULT NULL COMMENT 'Celular profesional salud',
  `correo` varchar(100) DEFAULT NULL COMMENT 'Correo profesional salud',
  `registro_profesional` varchar(50) DEFAULT NULL COMMENT 'Registro medico, puede ser NULL para recepcionistas/admins',
  `id_especialidad` int DEFAULT NULL COMMENT 'Referencia a ESPECIALIDADES',
  `id_centro_medico` int NOT NULL COMMENT 'Centro medico donde trabaja (Obligatorio)',
  `fecha_vinculacion` date DEFAULT (curdate()) COMMENT 'Fecha de vinculacion',
  `estado` enum('Activo','Inactivo','Vacaciones','Licencia') DEFAULT 'Activo' COMMENT 'Esta: activo, inactivo, etc',
  PRIMARY KEY (`id_profesional`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  UNIQUE KEY `uk_prof_doc` (`id_tipo_identificacion`,`numero_documento`),
  UNIQUE KEY `registro_profesional` (`registro_profesional`),
  KEY `id_genero` (`id_genero`),
  KEY `id_especialidad` (`id_especialidad`),
  KEY `id_centro_medico` (`id_centro_medico`),
  CONSTRAINT `profesional_salud_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `profesional_salud_ibfk_2` FOREIGN KEY (`id_tipo_identificacion`) REFERENCES `tipo_identificacion` (`id_tipo_identificacion`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `profesional_salud_ibfk_3` FOREIGN KEY (`id_genero`) REFERENCES `genero` (`id_genero`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `profesional_salud_ibfk_4` FOREIGN KEY (`id_especialidad`) REFERENCES `especialidades` (`id_especialidad`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `profesional_salud_ibfk_5` FOREIGN KEY (`id_centro_medico`) REFERENCES `centros_medicos` (`id_centro_medico`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profesional_salud`
--

LOCK TABLES `profesional_salud` WRITE;
/*!40000 ALTER TABLE `profesional_salud` DISABLE KEYS */;
/*!40000 ALTER TABLE `profesional_salud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `redes_salud`
--

DROP TABLE IF EXISTS `redes_salud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `redes_salud` (
  `id_red` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_red` varchar(150) NOT NULL COMMENT 'Nombre de la red: RIPSS (Redes integrales de prestadores de servicios de salud)',
  `descripcion` text COMMENT 'Descripcion',
  `id_region` int DEFAULT NULL COMMENT 'Referencia a REGION_SALUD',
  `estado_red` enum('Activa','Inactiva') DEFAULT 'Activa' COMMENT 'Esta activa, inactiva',
  PRIMARY KEY (`id_red`),
  UNIQUE KEY `nombre_red` (`nombre_red`),
  KEY `id_region` (`id_region`),
  CONSTRAINT `redes_salud_ibfk_1` FOREIGN KEY (`id_region`) REFERENCES `region_salud` (`id_region`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `redes_salud`
--

LOCK TABLES `redes_salud` WRITE;
/*!40000 ALTER TABLE `redes_salud` DISABLE KEYS */;
/*!40000 ALTER TABLE `redes_salud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region_salud`
--

DROP TABLE IF EXISTS `region_salud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region_salud` (
  `id_region` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_region` varchar(100) NOT NULL COMMENT 'Nombre de la region Ej: caribe, eje cafetero, sur occidente, etc',
  `descripcion` text COMMENT 'Descripcion',
  PRIMARY KEY (`id_region`),
  UNIQUE KEY `nombre_region` (`nombre_region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region_salud`
--

LOCK TABLES `region_salud` WRITE;
/*!40000 ALTER TABLE `region_salud` DISABLE KEYS */;
/*!40000 ALTER TABLE `region_salud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resultados_laboratorio`
--

DROP TABLE IF EXISTS `resultados_laboratorio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultados_laboratorio` (
  `id_resultado` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_paciente` int NOT NULL COMMENT 'Referencia a PACIENTES',
  `id_laboratorista` int DEFAULT NULL COMMENT 'Referencia al laboratorista-USUARIOS que registro',
  `id_servicio` int DEFAULT NULL COMMENT 'Referencia a SERVICIOS',
  `fecha_solicitud` date NOT NULL COMMENT 'Fecha en que se solicito el examen',
  `fecha_resultado` datetime DEFAULT NULL COMMENT 'Fecha en que se registro el resultado',
  `tipo_examen` varchar(200) NOT NULL COMMENT 'tipo de examenes solicitados',
  `resultado` text NOT NULL COMMENT 'Resultados de los examenes de laboratorio',
  `observaciones` text COMMENT 'Notas adicionales',
  `estado` enum('Pendiente','Registrado','Entregado') DEFAULT 'Pendiente' COMMENT 'Esta: pendiente, registrado, etc',
  `codigo_qr` varchar(255) DEFAULT NULL COMMENT 'Codigo QR para descarga',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro',
  PRIMARY KEY (`id_resultado`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_servicio` (`id_servicio`),
  KEY `id_laboratorista` (`id_laboratorista`),
  CONSTRAINT `resultados_laboratorio_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `resultados_laboratorio_ibfk_2` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_servicio`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `resultados_laboratorio_ibfk_3` FOREIGN KEY (`id_laboratorista`) REFERENCES `profesional_salud` (`id_profesional`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resultados_laboratorio`
--

LOCK TABLES `resultados_laboratorio` WRITE;
/*!40000 ALTER TABLE `resultados_laboratorio` DISABLE KEYS */;
/*!40000 ALTER TABLE `resultados_laboratorio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental del roles',
  `nombre_rol` varchar(50) NOT NULL COMMENT 'Nombre de los roles: paciente, profesional_salud, laboratorista, recepcionista, admin_centro_medico',
  `descripcion` text COMMENT 'Descripcion de los roles para mayor claridad, opcional',
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `nombre_rol` (`nombre_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `id_servicio` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental del servicio',
  `nombre_servicio` varchar(200) NOT NULL COMMENT 'Nombre del servicio medico',
  `descripcion` text COMMENT 'Descripcion detallada del servicio medico',
  `tipo_servicio` enum('Imagenologia','Laboratorio','Consulta Especialista','Control Médico','Procedimiento','Otro') NOT NULL COMMENT 'Categoria: imagenologia, laboratorio, etc',
  `id_especialidad` int DEFAULT NULL COMMENT 'Especialidad requerida (opcional)',
  `estado` enum('Activo','Inactivo','Suspendido') DEFAULT 'Activo' COMMENT 'Esta activo, inactivo, etc',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion',
  PRIMARY KEY (`id_servicio`),
  KEY `id_especialidad` (`id_especialidad`),
  CONSTRAINT `servicios_ibfk_1` FOREIGN KEY (`id_especialidad`) REFERENCES `especialidades` (`id_especialidad`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_identificacion`
--

DROP TABLE IF EXISTS `tipo_identificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_identificacion` (
  `id_tipo_identificacion` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `identificacion` varchar(50) NOT NULL COMMENT 'refiere al tipo de identificacion: cedula, tarjeta, etc',
  `nombre_identificacion` varchar(50) NOT NULL COMMENT 'Nombre de la abreviatura, CC: cedula de ciudadania',
  `descripcion` text COMMENT 'Descripcion opcional',
  PRIMARY KEY (`id_tipo_identificacion`),
  UNIQUE KEY `identificacion` (`identificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_identificacion`
--

LOCK TABLES `tipo_identificacion` WRITE;
/*!40000 ALTER TABLE `tipo_identificacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo_identificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_orden`
--

DROP TABLE IF EXISTS `tipo_orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_orden` (
  `id_tipo` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_tipo` varchar(50) NOT NULL COMMENT 'Es: Medicamentos, examenes, etc',
  PRIMARY KEY (`id_tipo`),
  UNIQUE KEY `nombre_tipo` (`nombre_tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_orden`
--

LOCK TABLES `tipo_orden` WRITE;
/*!40000 ALTER TABLE `tipo_orden` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo_orden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_afiliacion`
--

DROP TABLE IF EXISTS `tipos_afiliacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_afiliacion` (
  `id_tipo_afiliacion` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `nombre_tipo` varchar(20) NOT NULL COMMENT 'el paciente esta en regimen Contributivo, Subsidiado, etc',
  PRIMARY KEY (`id_tipo_afiliacion`),
  UNIQUE KEY `nombre_tipo` (`nombre_tipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_afiliacion`
--

LOCK TABLES `tipos_afiliacion` WRITE;
/*!40000 ALTER TABLE `tipos_afiliacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipos_afiliacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turnos`
--

DROP TABLE IF EXISTS `turnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turnos` (
  `id_turno` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental',
  `id_paciente` int NOT NULL COMMENT 'Referencia a PACIENTES',
  `id_profesional` int NOT NULL COMMENT 'Referencia a PROFESIONAL_SALUD',
  `id_centro_medico` int NOT NULL COMMENT 'Referencia a CENTROS_MEDICOS',
  `estado` enum('Programada','Atendida','Cancelada','No Asistio') DEFAULT 'Programada' COMMENT 'Esta: programada, atendido, etc',
  `fecha_hora_turno` datetime NOT NULL COMMENT 'Fecha y hora de la asignacion del turno',
  `solicitud_turno` enum('Remoto','En Sitio') DEFAULT 'Remoto' COMMENT 'Solicitado a partir de los 10m del centro medico',
  `categoria_turno` enum('Solicitar cita','Facturar cita','Laboratorios','Atencion al usuario','Consulta Medica') DEFAULT NULL COMMENT 'El paciente escoge la opcion',
  `modulo_asignado` varchar(100) DEFAULT NULL COMMENT 'Modulo asignado: Facturacion, Laboratorios, Atencion, etc',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro',
  PRIMARY KEY (`id_turno`),
  UNIQUE KEY `uk_turno_profesional` (`fecha_hora_turno`,`id_profesional`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_profesional` (`id_profesional`),
  KEY `id_centro_medico` (`id_centro_medico`),
  CONSTRAINT `turnos_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `turnos_ibfk_2` FOREIGN KEY (`id_profesional`) REFERENCES `profesional_salud` (`id_profesional`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `turnos_ibfk_3` FOREIGN KEY (`id_centro_medico`) REFERENCES `centros_medicos` (`id_centro_medico`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnos`
--

LOCK TABLES `turnos` WRITE;
/*!40000 ALTER TABLE `turnos` DISABLE KEYS */;
/*!40000 ALTER TABLE `turnos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincremental del usuario',
  `id_rol` int NOT NULL COMMENT 'Rol asignado para pacientes, profesional salud, recepcionista, laboratorista, adm centro',
  `nombre_usuario` varchar(50) NOT NULL COMMENT 'Login unico para el usuario',
  `contrasena` varchar(255) NOT NULL COMMENT 'Contrasena que crea el usuario',
  `email` varchar(100) DEFAULT NULL COMMENT 'Correo principal/login del usuario',
  `ultimo_login` datetime DEFAULT NULL COMMENT 'ultimo inicio de sesion',
  `estado` enum('Activo','Inactivo','Bloqueado') DEFAULT 'Activo' COMMENT 'Esta: activo, inactivo,etc',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 17:28:29
