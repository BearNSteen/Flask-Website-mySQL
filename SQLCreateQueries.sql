-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 14, 2021 at 06:34 PM
-- Server version: 10.4.17-MariaDB-log
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_glendond`
--

-- --------------------------------------------------------

--
-- Table structure for table `Consoles`
--

CREATE TABLE `Consoles` (
  `console_ID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `portable` tinyint(1) NOT NULL,
  `vr` tinyint(1) NOT NULL,
  `backwards_comp` tinyint(1) NOT NULL,
  `max_resolution` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Consoles`
--

INSERT INTO `Consoles` (`console_ID`, `name`, `company`, `portable`, `vr`, `backwards_comp`, `max_resolution`) VALUES
(1, 'Switch', 'Nintendo', 1, 1, 0, 1080),
(2, 'Playstation 5', 'Sony', 0, 1, 1, 4),
(4, 'Xbox Series', 'Microsoft', 0, 0, 1, 4),
(5, 'Xbox One', 'Microsoft', 0, 0, 1, 4),
(6, 'Playstation 4', 'Sony', 0, 1, 0, 4),
(7, 'Virtual Boy', 'Nintendo', 1, 1, 0, 720);

-- --------------------------------------------------------

--
-- Table structure for table `Console_Versions`
--

CREATE TABLE `Console_Versions` (
  `item_ID` int(11) NOT NULL,
  `game` int(11) NOT NULL,
  `console` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Console_Versions`
--

INSERT INTO `Console_Versions` (`item_ID`, `game`, `console`, `quantity`) VALUES
(8, 14, 1, 14),
(9, 15, 1, 7),
(10, 16, 1, 7),
(22, 4, 1, 5),
(23, 4, 2, 5),
(24, 4, 4, 5),
(25, 4, 5, 5),
(26, 4, 6, 5),
(27, 23, 4, 5),
(28, 23, 5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Games`
--

CREATE TABLE `Games` (
  `game_ID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `player_count` int(11) NOT NULL,
  `rating` char(1) NOT NULL,
  `online` tinyint(1) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `genre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Games`
--

INSERT INTO `Games` (`game_ID`, `title`, `player_count`, `rating`, `online`, `publisher`, `genre`) VALUES
(4, 'Tetris', 1, 'E', 1, 'Enhance', 'Puzzle'),
(5, 'Super Mario Sunshine', 2, 'E', 1, 'Nintendo', '3D Platformer'),
(6, 'Pikmin 2', 0, 'C', 0, '', 'Strategy'),
(7, 'LoZ Wind Waker', 0, 'C', 0, '', 'Action-Adventure'),
(8, 'Crash Bandicoot 4: It\'s About Time', 1, 'E', 0, 'Activision', '3D Platformer'),
(13, 'sss', 0, 'C', 0, '', 'Unknown'),
(14, 'Wario Land', 0, 'E', 0, '', 'Action-Adventure'),
(15, 'Super Mario Bros. 2', 0, 'E', 0, '', 'Action-Adventure'),
(16, 'Super Mario Bros. 3', 0, 'E', 0, '', 'Action-Adventure'),
(23, 'Halo', 4, 'T', 0, 'Microsoft', 'First-Person Shooter');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Consoles`
--
ALTER TABLE `Consoles`
  ADD PRIMARY KEY (`console_ID`);

--
-- Indexes for table `Console_Versions`
--
ALTER TABLE `Console_Versions`
  ADD PRIMARY KEY (`item_ID`),
  ADD KEY `game` (`game`),
  ADD KEY `console` (`console`);

--
-- Indexes for table `Games`
--
ALTER TABLE `Games`
  ADD PRIMARY KEY (`game_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Consoles`
--
ALTER TABLE `Consoles`
  MODIFY `console_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `Console_Versions`
--
ALTER TABLE `Console_Versions`
  MODIFY `item_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `Games`
--
ALTER TABLE `Games`
  MODIFY `game_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Console_Versions`
--
ALTER TABLE `Console_Versions`
  ADD CONSTRAINT `Console_Versions_ibfk_1` FOREIGN KEY (`game`) REFERENCES `Games` (`game_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Console_Versions_ibfk_2` FOREIGN KEY (`console`) REFERENCES `Consoles` (`console_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
