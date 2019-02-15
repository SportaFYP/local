CREATE DATABASE  IF NOT EXISTS `sportadb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `sportadb`;
-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: sportadb
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `matchdetails`
--

DROP TABLE IF EXISTS `matchdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `matchdetails` (
  `MatchID` int(11) NOT NULL,
  `matchname` varchar(45) NOT NULL,
  `teamID` varchar(45) NOT NULL,
  `studentName` varchar(100) NOT NULL,
  `tagID` varchar(45) NOT NULL,
  PRIMARY KEY (`MatchID`,`studentName`,`tagID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `matches` (
  `MatchID` int(11) NOT NULL AUTO_INCREMENT,
  `matchname` varchar(45) NOT NULL,
  `matchdate` datetime NOT NULL,
  `administrator` varchar(45) NOT NULL,
  `matchnotes` varchar(500) NOT NULL,
  `courtsize` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`MatchID`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matchinfo`
--

DROP TABLE IF EXISTS `matchinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `matchinfo` (
  `matchInfoID` int(11) NOT NULL AUTO_INCREMENT,
  `matchID` int(11) NOT NULL,
  `matchname` varchar(45) NOT NULL,
  `teamID` varchar(45) NOT NULL,
  `studentID` varchar(45) DEFAULT NULL,
  `studentName` varchar(100) NOT NULL,
  `playerNum` int(11) NOT NULL,
  `tagID` varchar(45) NOT NULL,
  PRIMARY KEY (`matchInfoID`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `new_table`
--

DROP TABLE IF EXISTS `new_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `new_table` (
  `studentID` varchar(20) NOT NULL,
  `studentName` varchar(50) NOT NULL,
  `uploadedDTG` datetime NOT NULL,
  `uploadedBy` varchar(50) NOT NULL,
  PRIMARY KEY (`studentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `overlay`
--

DROP TABLE IF EXISTS `overlay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `overlay` (
  `matchID` int(11) NOT NULL,
  `overlayData` longtext,
  PRIMARY KEY (`matchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `projects` (
  `number` int(11) NOT NULL AUTO_INCREMENT,
  `version` int(11) DEFAULT NULL,
  `tagId` int(11) NOT NULL,
  `RecordingID` int(11) NOT NULL,
  `success` int(11) DEFAULT NULL,
  `timestamp` decimal(12,2) DEFAULT NULL,
  `magnetic_x` decimal(10,0) DEFAULT NULL,
  `magnetic_y` decimal(10,0) DEFAULT NULL,
  `magnetic_z` decimal(10,0) DEFAULT NULL,
  `quaternion_x` decimal(10,0) DEFAULT NULL,
  `quaternion_y` decimal(10,0) DEFAULT NULL,
  `quaternion_z` decimal(10,0) DEFAULT NULL,
  `quaternion_w` decimal(10,0) DEFAULT NULL,
  `linearAcceleration_x` int(11) DEFAULT NULL,
  `linearAcceleration_y` int(11) DEFAULT NULL,
  `linearAcceleration_z` int(11) DEFAULT NULL,
  `pressure` decimal(10,0) DEFAULT NULL,
  `maxLinearAcceleration` int(11) DEFAULT NULL,
  `anchorData` int(11) DEFAULT NULL,
  `coordinates_x` int(11) DEFAULT NULL,
  `coordinates_y` int(11) DEFAULT NULL,
  `coordinates_z` int(11) DEFAULT NULL,
  `acceleration_x` decimal(10,0) DEFAULT NULL,
  `acceleration_y` decimal(10,0) DEFAULT NULL,
  `acceleration_z` decimal(10,0) DEFAULT NULL,
  `yaw` decimal(10,0) DEFAULT NULL,
  `roll` decimal(10,0) DEFAULT NULL,
  `pitch` decimal(10,0) DEFAULT NULL,
  `latency` text,
  PRIMARY KEY (`number`),
  KEY `RecordingID_idx` (`RecordingID`),
  CONSTRAINT `RecordingID` FOREIGN KEY (`RecordingID`) REFERENCES `recordings` (`recordingid`)
) ENGINE=InnoDB AUTO_INCREMENT=195445 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recordings`
--

DROP TABLE IF EXISTS `recordings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `recordings` (
  `RecordingID` int(11) NOT NULL AUTO_INCREMENT,
  `Match_ID` int(11) NOT NULL,
  `startTime` datetime NOT NULL,
  `endTime` datetime DEFAULT NULL,
  `saveFile` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`RecordingID`),
  KEY `MatchID_idx` (`startTime`),
  KEY `MatchID_idx1` (`Match_ID`),
  CONSTRAINT `Match_ID` FOREIGN KEY (`Match_ID`) REFERENCES `matches` (`matchid`)
) ENGINE=InnoDB AUTO_INCREMENT=667 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `student` (
  `studentID` varchar(20) NOT NULL,
  `studentName` varchar(50) NOT NULL,
  `uploadedDTG` datetime NOT NULL,
  `uploadedBy` varchar(50) NOT NULL,
  PRIMARY KEY (`studentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tags` (
  `TagNumber` varchar(30) NOT NULL,
  `TagId` int(11) DEFAULT NULL,
  `LastUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`TagNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `team` (
  `teamId` varchar(20) NOT NULL,
  `createdDTG` datetime NOT NULL,
  `createdBy` varchar(50) NOT NULL,
  PRIMARY KEY (`teamId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamstudent`
--

DROP TABLE IF EXISTS `teamstudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `teamstudent` (
  `teamId` varchar(20) NOT NULL,
  `studentID` varchar(20) NOT NULL,
  PRIMARY KEY (`studentID`,`teamId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-11  9:02:46
