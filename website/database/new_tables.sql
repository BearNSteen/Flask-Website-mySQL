CREATE TABLE `Consoles` (
  `console_ID` int(11) AUTO_INCREMENT NOT NULL,
  `name` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `portable` tinyint(1) NOT NULL,
  `vr` tinyint(1) NOT NULL,
  `backwards_comp` tinyint(1) NOT NULL,
  `max_resolution` int(11) NOT NULL,
  PRIMARY KEY (`console_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Games` (
  `game_ID` int(11) AUTO_INCREMENT NOT NULL,
  `title` varchar(255) NOT NULL,
  `player_count` int(11) NOT NULL,
  `rating` char(1) NOT NULL,
  `online` tinyint(1) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `genre` varchar(255) NOT NULL,
  PRIMARY KEY (`game_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Console_Versions` (
  `item_ID` int(11) AUTO_INCREMENT NOT NULL,
  `game` int(11) NOT NULL,
  `console` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY(`item_ID`),
  FOREIGN KEY (`game`) REFERENCES `Games` (`game_ID`) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`console`) REFERENCES `Consoles` (`console_ID`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Customers` (
  `customer_ID` int(11) AUTO_INCREMENT NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` int(11) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `birthday` date NOT NULL,
  PRIMARY KEY (`customer_ID`),
  UNIQUE KEY `full_name` (`first_name`,`last_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Rentals` (
  `rental_ID` int(11) AUTO_INCREMENT NOT NULL,
  `customer` int(11) NOT NULL,
  `rent_date` date NOT NULL,
  `paid` tinyint(1) NOT NULL,
  PRIMARY KEY (`rental_ID`),
  FOREIGN KEY (`customer`) REFERENCES `Customers` (`customer_ID`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Game_Rentals` (
  `game_version` int(11) NOT NULL,
  `rental` int(11) NOT NULL,
  PRIMARY KEY (`game_version`, `rental`),
  FOREIGN KEY (`game_version`) REFERENCES `Console_Versions` (`item_ID`) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`rental`) REFERENCES `Rentals` (`rental_ID`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Customers (first_name, last_name, street, state, zip, phone, email, birthday, city) VALUES ('bob', 'dole', '123 street', 'ny', '12345', '123456789', 'me@you.com', '1990-01-01', 'ny');
INSERT INTO Rentals (customer, rent_date, paid) VALUES ('1', '2021-02-02', '0');
INSERT INTO Games (title, publisher, player_count, rating, online, genre) VALUES ('Super Mario Bros.', 'Nintendo', '2', 'E', '0', 'Platformer');
INSERT INTO Consoles (name, company, portable, vr, backwards_comp, max_resolution) VALUES ('Switch', 'Nintendo', '1', '1', '0', '1080');
INSERT INTO Console_Versions (game, console, quantity) VALUES ('1', '1', '5');
INSERT INTO Game_Rentals (game_version, rental) VALUES ('1', '1');