-- Group 49 functionalities

-- get all information on Games
SELECT * FROM Games;

-- get all information on Consoles
SELECT * FROM Consoles;

-- get all information on Rentals
SELECT * FROM Rentals;

-- get all information on Customers
SELECT * FROM Customers;

-- get all Console_Versions for a particular Game
SELECT Games.title, Consoles.name, Console_Versions.quantity FROM Games INNER JOIN Console_Versions ON Games.game_ID = Console_Versions.game 
INNER JOIN Consoles ON Console_Versions.console = Consoles.console_ID WHERE Games.game_ID = :game_IDinput;

-- get all Console_Versions for a particular Console
SELECT Games.title, Consoles.name, Console_Versions.quantity FROM Games INNER JOIN Console_Versions ON Games.game_ID = Console_Versions.game 
INNER JOIN Consoles ON Console_Versions.console = Consoles.console_ID WHERE Consoles.console_ID = :console_IDinput;

-- get all Game_Rentals for a particular Rental
SELECT Games.title, Consoles.name, Rentals.rental_ID FROM Rentals INNER JOIN Game_Rentals ON Game_Rentals.rental = Rentals.rental_ID 
INNER JOIN Console_Versions ON Console_Versions.item_ID = Game_Rentals.game_version INNER JOIN Games ON Console_Versions.game = Games.game_ID 
INNER JOIN Consoles ON Console_Versions.console = Consoles.console_ID WHERE Rentals.rental_ID = :rental_IDinput;

-- get all Rentals for a particular Customer
SELECT Rentals.rental_ID, Customers.first_name, Customers.last_name FROM Rentals INNER JOIN Customers ON Rentals.customer = Customers.customer_ID WHERE Customers.customer_ID = :customer_IDinput;

-- add a new Game
INSERT INTO Games (title, player_count, rating, online, publisher, genre) VALUES (:titleInput, :player_countInput, :ratingInput, :onlineInput, :publisherInput, :genreInput); 

-- add a new Console
INSERT INTO Console (name, company, portable, vr, backwards_comp, max_resolution) VALUES (:nameInput, :companyInput, :portableInput, :vrInput, :backwards_compInput, :max_resolutionInput); 

-- add a new Rental
INSERT INTO Rentals (customer, item_count, rent_date, cost) VALUES (:customerInput, :item_countInput, :rent_dateInput, :costInput); 

-- add a new Customer
INSERT INTO Customers (first_name, last_name, street, city, state, zip, phone, email, birthday) VALUES (:first_nameInput, :last_nameInput, :streetInput, :cityInput, :stateInput, :zipInput, :phoneInput, :emailInput, :birthdayInput)

-- update a Game 
UPDATE Games SET title = :titleInput, player_count = :player_countInput, rating = :ratingInput, online = :onlineInput, publisher = :publisherInput, genre = :genreInput WHERE game_ID = :game_IDinput;

-- update a Console
UPDATE Console SET name = :nameInput, company = :companyInput, portable = :portableInput, vr = :vrInput, backwards_comp = :backwards_compInput, max_resolution = :max_resolutionInput WHERE console_ID = :console_IDinput;

-- update a Rental
UPDATE Rentals SET customer = :customerInput, item_count = :item_countInput, rent_date = :rent_dateInput, cost = :costInput WHERE rental_ID = :rental_IDinput;

-- update a Customer
UPDATE Customers SET first_name = :first_nameInput, last_name = :last_nameInput, street = :streetInput, city = :cityInput, state = :stateInput, zip = :zipInput, phone = :phoneInput, email = :emailInput, birthday = :birthdayInput WHERE customer_ID = :customer_IDinput;

-- delete a Game
DELETE FROM Games WHERE game_ID = :game_ID_selected_from_browse_character_page

-- delete a Console
DELETE FROM Consoles WHERE console_ID = :console_ID_selected_from_browse_character_page

-- delete a Rental
DELETE FROM Rentals WHERE rental_ID = :rental_ID_selected_from_browse_character_page

-- delete a Customer
DELETE FROM bsg_people WHERE customer_ID = :customer_ID_selected_from_browse_character_page

