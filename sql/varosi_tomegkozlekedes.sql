-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 22, 2020 at 06:01 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `varosi_tomegkozlekedes`
--

-- --------------------------------------------------------

--
-- Table structure for table `indul`
--

CREATE TABLE `indul` (
  `rendszam` char(6) NOT NULL,
  `vonal_nev` varchar(255) NOT NULL,
  `visszamenet` tinyint(1) NOT NULL,
  `mikor` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `indul`
--

INSERT INTO `indul` (`rendszam`, `vonal_nev`, `visszamenet`, `mikor`) VALUES
('HAF097', '3', 0, '08:00:00'),
('NKX525', '3', 1, '08:00:00'),
('SAT888', '3', 0, '09:00:00'),
('VUM973', '3', 1, '09:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `jarat`
--

CREATE TABLE `jarat` (
  `vonal_nev` varchar(255) NOT NULL,
  `visszamenet` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jarat`
--

INSERT INTO `jarat` (`vonal_nev`, `visszamenet`) VALUES
('13', 0),
('13', 1),
('16', 0),
('16', 1),
('19', 0),
('19', 1),
('23', 0),
('23', 1),
('26', 0),
('26', 1),
('29', 0),
('29', 1),
('3', 0),
('3', 1),
('33', 0),
('33', 1),
('36', 0),
('36', 1),
('39', 0),
('39', 1),
('6', 0),
('6', 1),
('9', 0),
('9', 1);

-- --------------------------------------------------------

--
-- Table structure for table `jarmu`
--

CREATE TABLE `jarmu` (
  `rendszam` char(6) NOT NULL,
  `alacsony_padlos` tinyint(1) NOT NULL,
  `tipus_nev` varchar(255) NOT NULL,
  `vezetoi_szam` char(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jarmu`
--

INSERT INTO `jarmu` (`rendszam`, `alacsony_padlos`, `tipus_nev`, `vezetoi_szam`) VALUES
('AWA515', 0, 'busz', '001'),
('EMP111', 1, 'troli', '008'),
('FAZ516', 0, 'busz', '003'),
('GGM391', 0, 'busz', '020'),
('HAF097', 0, 'villamos', '024'),
('ICI772', 1, 'busz', '016'),
('MAR246', 1, 'busz', '002'),
('NKX525', 1, 'villamos', '017'),
('SAT888', 1, 'villamos', '007'),
('TKR654', 0, 'troli', '011'),
('VUM973', 0, 'villamos', '008'),
('WUU812', 0, 'troli', '006'),
('ZZH425', 1, 'busz', '005');

-- --------------------------------------------------------

--
-- Table structure for table `jarmutipus`
--

CREATE TABLE `jarmutipus` (
  `nev` varchar(255) NOT NULL,
  `elektromos` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jarmutipus`
--

INSERT INTO `jarmutipus` (`nev`, `elektromos`) VALUES
('busz', 0),
('troli', 1),
('villamos', 1);

-- --------------------------------------------------------

--
-- Table structure for table `megall`
--

CREATE TABLE `megall` (
  `vonal_nev` varchar(255) NOT NULL,
  `visszamenet` tinyint(1) NOT NULL,
  `megallo_id` int(11) NOT NULL,
  `mikor` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `megall`
--

INSERT INTO `megall` (`vonal_nev`, `visszamenet`, `megallo_id`, `mikor`) VALUES
('3', 0, 13, '00:15:00'),
('3', 0, 14, '00:00:00'),
('3', 0, 19, '00:10:00'),
('3', 0, 29, '00:25:00'),
('3', 0, 30, '00:05:00'),
('3', 0, 32, '00:20:00'),
('3', 1, 13, '00:10:00'),
('3', 1, 14, '00:25:00'),
('3', 1, 19, '00:15:00'),
('3', 1, 30, '00:20:00'),
('3', 1, 32, '00:05:00'),
('6', 1, 29, '00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `megallo`
--

CREATE TABLE `megallo` (
  `id` int(11) NOT NULL,
  `nev` varchar(255) NOT NULL,
  `hely` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `megallo`
--

INSERT INTO `megallo` (`id`, `nev`, `hely`) VALUES
(1, 'Pista utca', 'Pista utca 27/a. előtt'),
(2, 'Kerekes út', 'Kerekes út 163/d. előtt'),
(3, 'Hosszú utca', 'Hosszú utca 643 előtt'),
(4, 'Könyék utca', 'Könyék utca 3.'),
(5, 'Bölcsességfog tér', 'Fog sor 8.'),
(6, 'Keresztcsont', 'Gerinc utca 25.'),
(7, 'Kőzet utca', 'Kőzet utca 2. előtt'),
(8, 'Sándor utca', 'Sándor utca 13. előtt'),
(9, 'Hortobágyi út', 'Hortobágyi út 102. előtt'),
(10, 'Pécsi út', 'Pécsi út 19. előtt'),
(11, 'Somodi út', 'Somodi út 69. előtt'),
(12, 'Bodor utca', 'Bodor utca 67. előtt'),
(13, 'Horvát tér', 'Horvát tér 12.'),
(14, 'Bal kamra', 'Szívtér 3.'),
(15, 'Város körút', 'Város körút 435.'),
(16, 'Gauss', 'Maxwell törvények 2.'),
(17, 'Angyal út', 'Angyal út 567. előtt'),
(18, 'Cinege utca', 'Cinege utca 76. előtt'),
(19, 'Csóri utca', 'Csóri utca és Csíra utca sarkán'),
(20, 'Murmur', 'Ars Goetia 19.'),
(21, 'Dobó utca', 'Dobó utca 44. előtt'),
(22, 'Ameretat', 'Amesha Spentas 7.'),
(23, 'Ementali körút', 'Ementali körűt és Lyukas utca sarkán'),
(24, 'Dzsumbuj utca', 'Dzsumbuj utca 22. előtt'),
(25, 'Értéktelen tér', 'Értéktelen tér 1.'),
(26, 'Fény', 'Vég utca 100.'),
(27, 'Ortogonalitás', 'Euklideszi tér 2.'),
(28, 'Standard', 'X utca 100., Y utca 10., és Z utca 1. sarkán'),
(29, 'Xadkilencperkilencfaktor', 'Szinusz sor 4.'),
(30, 'A két torony', 'Gyűrűk utca 2.'),
(31, 'Kalapács tér', 'Kalapács tér 21. előtt'),
(32, 'Levantei út', 'Levantei út 77.');

-- --------------------------------------------------------

--
-- Table structure for table `vezeto`
--

CREATE TABLE `vezeto` (
  `vezetoi_szam` char(3) NOT NULL,
  `vezeteknev` varchar(255) NOT NULL,
  `keresztnev` varchar(255) NOT NULL,
  `szul_datum` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `vezeto`
--

INSERT INTO `vezeto` (`vezetoi_szam`, `vezeteknev`, `keresztnev`, `szul_datum`) VALUES
('001', 'Alattomos', 'Aladár', '1987-11-11'),
('002', 'Álmos', 'Álmos', '1971-03-25'),
('003', 'Béna', 'Béla', '1960-06-07'),
('004', 'Cinikus', 'Cecília', '1989-08-09'),
('005', 'Csacsogó', 'Csaba', '1997-02-27'),
('006', 'Dilinyós', 'Dömötör', '1963-04-14'),
('007', 'Elmebeteg', 'Előd', '1988-07-12'),
('008', 'Érdekes', 'Éva', '1991-12-25'),
('009', 'Fenyegető', 'Ferenc', '2001-09-11'),
('010', 'Gurgulázó', 'Géza', '1981-08-18'),
('011', 'Gyerekes', 'Gyöngyi', '1979-09-05'),
('012', 'Hajlandó', 'Helga', '1969-06-09'),
('013', 'Izgága', 'Irén', '1968-11-30'),
('014', 'Ígéretes', 'Ízisz', '1984-08-04'),
('015', 'Joó', 'Jézus', '1994-07-21'),
('016', 'Kovács', 'Krisztián', '1971-01-01'),
('017', 'Levantei', 'Levente', '2000-02-20'),
('018', 'Lyukas', 'Lyános', '1986-04-26'),
('019', 'Mártír', 'Márta', '1977-05-08'),
('020', 'Nosza', 'Nóra', '1996-07-08'),
('021', 'Nyikorgó', 'Nyina', '1998-08-19'),
('022', 'Orángután', 'Ottó', '1970-10-10'),
('023', 'Óriási', 'Óren', '1988-02-02'),
('024', 'Örömteli', 'Özséb', '1966-03-14'),
('025', 'Őr', 'Őze', '2001-12-21');

-- --------------------------------------------------------

--
-- Table structure for table `vonal`
--

CREATE TABLE `vonal` (
  `nev` varchar(255) NOT NULL,
  `hossz` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `vonal`
--

INSERT INTO `vonal` (`nev`, `hossz`) VALUES
('13', 4),
('16', 8),
('19', 5),
('23', 6),
('26', 6),
('29', 7),
('3', 5),
('33', 10),
('36', 4),
('39', 10),
('43', 3),
('46', 11),
('49', 7),
('53', 7),
('56', 6),
('59', 5),
('6', 8),
('63', 5),
('66', 9),
('69', 7),
('73', 4),
('76', 14),
('79', 8),
('9', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `indul`
--
ALTER TABLE `indul`
  ADD PRIMARY KEY (`rendszam`,`vonal_nev`,`visszamenet`),
  ADD KEY `vonal_nev` (`vonal_nev`,`visszamenet`);

--
-- Indexes for table `jarat`
--
ALTER TABLE `jarat`
  ADD PRIMARY KEY (`vonal_nev`,`visszamenet`);

--
-- Indexes for table `jarmu`
--
ALTER TABLE `jarmu`
  ADD PRIMARY KEY (`rendszam`),
  ADD KEY `vezetoi_szam` (`vezetoi_szam`),
  ADD KEY `tipus_nev` (`tipus_nev`);

--
-- Indexes for table `jarmutipus`
--
ALTER TABLE `jarmutipus`
  ADD PRIMARY KEY (`nev`);

--
-- Indexes for table `megall`
--
ALTER TABLE `megall`
  ADD PRIMARY KEY (`vonal_nev`,`visszamenet`,`megallo_id`),
  ADD KEY `megallo_id` (`megallo_id`);

--
-- Indexes for table `megallo`
--
ALTER TABLE `megallo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `vezeto`
--
ALTER TABLE `vezeto`
  ADD PRIMARY KEY (`vezetoi_szam`);

--
-- Indexes for table `vonal`
--
ALTER TABLE `vonal`
  ADD PRIMARY KEY (`nev`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `megallo`
--
ALTER TABLE `megallo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `indul`
--
ALTER TABLE `indul`
  ADD CONSTRAINT `indul_ibfk_1` FOREIGN KEY (`rendszam`) REFERENCES `jarmu` (`rendszam`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `indul_ibfk_2` FOREIGN KEY (`vonal_nev`,`visszamenet`) REFERENCES `jarat` (`vonal_nev`, `visszamenet`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `jarat`
--
ALTER TABLE `jarat`
  ADD CONSTRAINT `jarat_ibfk_1` FOREIGN KEY (`vonal_nev`) REFERENCES `vonal` (`nev`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `jarmu`
--
ALTER TABLE `jarmu`
  ADD CONSTRAINT `jarmu_ibfk_1` FOREIGN KEY (`vezetoi_szam`) REFERENCES `vezeto` (`vezetoi_szam`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `jarmu_ibfk_2` FOREIGN KEY (`tipus_nev`) REFERENCES `jarmutipus` (`nev`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `megall`
--
ALTER TABLE `megall`
  ADD CONSTRAINT `megall_ibfk_1` FOREIGN KEY (`vonal_nev`,`visszamenet`) REFERENCES `jarat` (`vonal_nev`, `visszamenet`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `megall_ibfk_2` FOREIGN KEY (`megallo_id`) REFERENCES `megallo` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
