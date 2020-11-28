-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2020 at 12:03 PM
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
('ARN394', '13', 0, '01:00:00'),
('EFO354', '13', 0, '01:20:00'),
('IHG969', '13', 0, '01:40:00'),
('MLC847', '13', 0, '00:00:00'),
('BLE039', '13', 1, '01:00:00'),
('ICZ341', '13', 1, '01:20:00'),
('IUJ004', '13', 1, '01:40:00'),
('NAN887', '13', 1, '00:00:00'),
('GYF022', '16', 0, '12:00:00'),
('IRG463', '16', 0, '20:00:00'),
('MTV658', '16', 0, '14:00:00'),
('PTF833', '16', 0, '14:00:00'),
('XTP520', '16', 0, '18:00:00'),
('GYF022', '16', 1, '18:00:00'),
('IRG463', '16', 1, '12:00:00'),
('MTV658', '16', 1, '20:00:00'),
('OIH551', '16', 1, '14:00:00'),
('TCM942', '16', 1, '16:00:00'),
('HAF097', '3', 0, '08:00:00'),
('NKX525', '3', 0, '10:00:00'),
('SAT888', '3', 0, '09:00:00'),
('HAF097', '3', 1, '10:00:00'),
('NKX525', '3', 1, '08:00:00'),
('VUM973', '3', 1, '09:00:00'),
('AWA515', '6', 0, '12:00:00'),
('CEU131', '6', 0, '14:00:00'),
('FAZ516', '6', 0, '16:00:00'),
('GBU213', '6', 0, '18:00:00'),
('AWA515', '6', 1, '16:00:00'),
('CEU131', '6', 1, '18:00:00'),
('HTG607', '6', 1, '12:00:00'),
('JRY107', '6', 1, '14:00:00'),
('DVO758', '9', 0, '20:00:00'),
('NDP699', '9', 0, '21:00:00'),
('PFS653', '9', 0, '22:00:00'),
('EMP111', '9', 1, '20:00:00'),
('OGV424', '9', 1, '21:00:00'),
('RUW281', '9', 1, '22:00:00');

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
('3', 0),
('3', 1),
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
('ARN394', 1, 'villamos', '040'),
('AWA515', 0, 'busz', '001'),
('BLE039', 0, 'villamos', '010'),
('CEU131', 1, 'busz', '004'),
('DVO758', 1, 'troli', '019'),
('EFO354', 1, 'villamos', '016'),
('EMP111', 1, 'troli', '008'),
('FAZ516', 0, 'busz', '003'),
('GBU213', 0, 'busz', '006'),
('GYF022', 1, 'busz', '025'),
('HAF097', 0, 'villamos', '024'),
('HTG607', 0, 'busz', '002'),
('ICZ341', 1, 'villamos', '009'),
('IHG969', 0, 'villamos', '042'),
('IRG463', 1, 'busz', '012'),
('IUJ004', 0, 'villamos', '023'),
('JRY107', 1, 'busz', '005'),
('MLC847', 1, 'villamos', '044'),
('MTV658', 1, 'busz', '018'),
('NAN887', 1, 'villamos', '013'),
('NDP699', 1, 'troli', '028'),
('NKX525', 1, 'villamos', '017'),
('OGV424', 1, 'troli', '037'),
('OIH551', 1, 'busz', '021'),
('PFS653', 0, 'troli', '022'),
('PTF833', 0, 'busz', '043'),
('RUW281', 0, 'troli', '015'),
('SAT888', 1, 'villamos', '007'),
('TCM942', 0, 'busz', '036'),
('TKR654', 0, 'troli', '011'),
('UTQ382', 0, 'busz', '020'),
('VSL903', 0, 'troli', '030'),
('VUM973', 0, 'villamos', '008'),
('XTP520', 0, 'busz', '014');

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
('13', 0, 1, '00:00:00'),
('13', 0, 2, '00:03:00'),
('13', 0, 3, '00:06:00'),
('13', 0, 8, '00:08:00'),
('13', 0, 9, '00:20:00'),
('13', 0, 10, '00:12:00'),
('13', 0, 18, '00:14:00'),
('13', 0, 29, '00:16:00'),
('13', 1, 1, '00:20:00'),
('13', 1, 2, '00:17:00'),
('13', 1, 3, '00:14:00'),
('13', 1, 8, '00:12:00'),
('13', 1, 9, '00:00:00'),
('13', 1, 10, '00:08:00'),
('13', 1, 18, '00:06:00'),
('13', 1, 29, '00:04:00'),
('16', 0, 4, '00:24:00'),
('16', 0, 12, '00:19:00'),
('16', 0, 16, '00:21:00'),
('16', 0, 17, '00:00:00'),
('16', 0, 18, '00:03:00'),
('16', 0, 21, '00:07:00'),
('16', 0, 30, '00:28:00'),
('16', 0, 40, '00:11:00'),
('16', 0, 41, '00:16:00'),
('16', 1, 4, '00:04:00'),
('16', 1, 12, '00:09:00'),
('16', 1, 16, '00:07:00'),
('16', 1, 17, '00:28:00'),
('16', 1, 18, '00:25:00'),
('16', 1, 21, '00:21:00'),
('16', 1, 30, '00:00:00'),
('16', 1, 40, '00:17:00'),
('16', 1, 41, '00:12:00'),
('3', 0, 9, '00:20:00'),
('3', 0, 12, '00:22:00'),
('3', 0, 13, '00:10:30'),
('3', 0, 14, '00:00:00'),
('3', 0, 19, '00:07:00'),
('3', 0, 29, '00:17:30'),
('3', 0, 30, '00:03:00'),
('3', 0, 32, '00:15:00'),
('3', 0, 37, '00:27:30'),
('3', 1, 9, '00:07:30'),
('3', 1, 12, '00:05:30'),
('3', 1, 13, '00:17:00'),
('3', 1, 14, '00:27:30'),
('3', 1, 19, '00:20:30'),
('3', 1, 29, '00:10:00'),
('3', 1, 30, '00:24:30'),
('3', 1, 32, '00:12:30'),
('3', 1, 37, '00:00:00'),
('6', 0, 6, '00:00:00'),
('6', 0, 7, '00:07:00'),
('6', 0, 11, '00:14:00'),
('6', 0, 24, '00:24:00'),
('6', 0, 27, '00:10:00'),
('6', 0, 28, '00:16:00'),
('6', 0, 42, '00:21:00'),
('6', 1, 6, '00:24:00'),
('6', 1, 7, '00:17:00'),
('6', 1, 11, '00:10:00'),
('6', 1, 24, '00:00:00'),
('6', 1, 27, '00:14:00'),
('6', 1, 28, '00:08:00'),
('6', 1, 42, '00:03:00'),
('9', 0, 15, '00:07:00'),
('9', 0, 20, '00:19:00'),
('9', 0, 22, '00:21:00'),
('9', 0, 23, '00:09:00'),
('9', 0, 26, '00:25:00'),
('9', 0, 31, '00:12:00'),
('9', 0, 38, '00:05:00'),
('9', 0, 39, '00:16:00'),
('9', 0, 43, '00:00:00'),
('9', 1, 15, '00:18:00'),
('9', 1, 20, '00:06:00'),
('9', 1, 22, '00:04:00'),
('9', 1, 23, '00:16:00'),
('9', 1, 26, '00:00:00'),
('9', 1, 31, '00:13:00'),
('9', 1, 38, '00:20:00'),
('9', 1, 39, '00:09:00'),
('9', 1, 43, '00:25:00');

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
(26, 'Fény', 'Vég utca 100.'),
(27, 'Ortogonalitás', 'Euklideszi tér 2.'),
(28, 'Standard', 'X utca 100., Y utca 10., és Z utca 1. sarkán'),
(29, 'Xadkilencperkilencfaktor', 'Szinusz sor 4.'),
(30, 'A két torony', 'Gyűrűk utca 2.'),
(31, 'Kalapács tér', 'Kalapács tér 21. előtt'),
(32, 'Levantei út', 'Levantei út 77.'),
(37, 'Porter tér', 'Sör utca 69.'),
(38, 'Bokk', 'Savas utca és Bor tér sarkán'),
(39, 'Pacal', 'Pörkölt utca 11.'),
(40, 'Taylor sor', 'Taylor sor 0.'),
(41, 'Mordor tér', 'Mordor tér 666.'),
(42, 'Felts út', 'Stadion utca 6.'),
(43, 'Szingularitás', 'Tömeg utca 8.');

-- --------------------------------------------------------

--
-- Stand-in structure for view `menetrend`
-- (See below for the actual view)
--
CREATE TABLE `menetrend` (
`vonal` varchar(255)
,`visszamenet` tinyint(1)
,`megallo_nev` varchar(255)
,`mikor` time
);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `admin` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`, `email`, `admin`) VALUES
('admin', 'admin', 'admin@admin.com', 1),
('user', 'user', 'user@user.com', 0);

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
('025', 'Őr', 'Őze', '2001-12-21'),
('026', 'Pompás', 'Polixénia', '1996-09-06'),
('027', 'Ragyás', 'Radomér', '1969-03-27'),
('028', 'Sas', 'Slomó', '1984-07-08'),
('029', 'Szűz', 'Sztavrula', '1994-02-09'),
('030', 'Thot', 'Tasziló', '1999-09-09'),
('031', 'Tyúk', 'Teodolinda', '1979-04-20'),
('032', 'Uborkás', 'Ulászló', '1966-09-27'),
('033', 'Új', 'Údó', '1991-10-13'),
('034', 'Üdvös', 'Üdvöske', '1998-08-19'),
('035', 'Űr', 'Üllő', '1984-05-22'),
('036', 'Virgonc', 'Vérbulcsú', '2002-01-02'),
('037', 'Weöres', 'Wanessha', '2001-06-11'),
('038', 'Xilofon', 'Xerxész', '1960-01-01'),
('039', 'Yayy', 'Yanó', '1956-10-23'),
('040', 'Zádor', 'Zenobiusz', '1974-05-08'),
('041', 'Zsorzsett', 'Zsandark', '1990-12-31'),
('042', 'Dzsukáló', 'Dzsenifer', '2000-02-20'),
('043', 'Dzéta', 'Döníz', '1978-11-28'),
('044', 'Query', 'Qnó', '1974-05-03');

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
('13', 7),
('16', 9),
('19', 5),
('3', 5),
('6', 8),
('9', 4);

-- --------------------------------------------------------

--
-- Structure for view `menetrend`
--
DROP TABLE IF EXISTS `menetrend`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `menetrend`  AS  (select `megall`.`vonal_nev` AS `vonal`,`megall`.`visszamenet` AS `visszamenet`,lcase(`megallo`.`nev`) AS `megallo_nev`,`megall`.`mikor` AS `mikor` from (`megall` join `megallo` on(`megall`.`megallo_id` = `megallo`.`id`)) order by `megall`.`vonal_nev`,`megall`.`visszamenet`,`megall`.`mikor`) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `indul`
--
ALTER TABLE `indul`
  ADD PRIMARY KEY (`rendszam`,`mikor`),
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
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

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
