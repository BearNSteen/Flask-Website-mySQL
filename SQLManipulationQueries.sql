SELECT title, player_count, rating, online, publisher, genre, game_id FROM Games;

SELECT game_ID, title, name, quantity, (quantity - COUNT(game_version)) as available FROM Console_Versions 
INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID 
LEFT JOIN Game_Rentals ON item_ID = game_version GROUP BY item_ID;

SELECT name, console_id FROM Consoles;

SELECT title FROM Games WHERE title = [:title];

INSERT INTO Games (title, player_count, rating, online, publisher, genre) VALUES (%s,%s,%s,%s,%s,%s);

SELECT console_id FROM Consoles WHERE name = [:console_name];

SELECT game FROM Console_Versions WHERE game = [:game_id] AND console = [:console_id];

INSERT INTO Console_Versions (game, console, quantity) VALUES (%s,%s,%s);

UPDATE Console_Versions SET quantity = [:quantity] WHERE game = [:game_id];

SELECT name FROM Consoles;

SELECT g.game_id, g.title, g.player_count, g.rating, g.publisher, g.genre FROM Games g 
INNER JOIN Console_Versions cv ON g.game_ID = cv.game INNER JOIN Consoles c ON cv.console = c.console_ID WHERE [:filter_conditions];

SELECT console_id FROM Consoles WHERE name = [:name];

SELECT game_ID, title, name, quantity, (quantity - COUNT(game_version)) as available FROM Console_Versions
INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID 
LEFT JOIN Game_Rentals ON item_ID = game_version GROUP BY item_ID;

SELECT name, console_id FROM Consoles;

DELETE FROM Games WHERE game_ID = %s;

UPDATE Games SET title = %s, player_count = %s, rating = %s, online = %s, publisher = %s, genre = %s WHERE game_id = %s

SELECT name, company, portable, vr, backwards_comp, max_resolution, console_id FROM Consoles;

SELECT console_id, title, name, quantity, (quantity - COUNT(game_version)) as available FROM Console_Versions
INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals
ON item_ID = game_version GROUP BY item_ID;

SELECT name, company, portable, vr, backwards_comp, max_resolution FROM Consoles;

INSERT INTO Consoles (name, company, portable, vr, backwards_comp, max_resolution) VALUES (%s,%s,%s,%s,%s,%s);

SELECT c.name, c.company, c.portable, c.vr, c.backwards_comp, c.max_resolution FROM Consoles c 
INNER JOIN Console_Versions cv ON c.console_ID = cv.console INNER JOIN Games g ON cv.console = c.console_ID WHERE [:conditions];

DELETE FROM Consoles WHERE console_ID = %s;

SELECT * FROM Consoles WHERE console_id = %s

UPDATE Consoles SET name = %s, company = %s, portable = %s, vr = %s, backwards_comp = %s, max_resolution = %s WHERE console_id = %s

SELECT rental_ID, first_name, last_name, DATE_FORMAT(rent_date, '%%b %%e %%Y') as date, DATE_FORMAT(paid, '%%b %%e %%Y') as paid,
COUNT(game_version) as rentals, COUNT(game_version) * '4.99' as cost, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') as due,
CASE WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid
THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) END AS days_late, CASE WHEN COUNT(game_version) = '0' THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL
THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid THEN '0.00'
ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END AS late_fee, ((COUNT(game_version) * '4.99') + (CASE WHEN COUNT(game_version) = '0' THEN '0.00'
WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid
THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END)) as total FROM Rentals INNER JOIN Customers ON customer = customer_ID
LEFT JOIN Game_Rentals ON rental_ID = rental GROUP BY rental_ID;

SELECT game_version, rental, title, name FROM Game_Rentals INNER JOIN Console_Versions on game_version = item_ID
INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID;

SELECT title, name FROM Games INNER JOIN Console_Versions ON game_ID = game INNER JOIN Consoles ON console = console_ID;

SELECT first_name, last_name FROM Customers INNER JOIN Rentals ON customer_ID = customer;

SELECT game_version, rental, title, name FROM Game_Rentals INNER JOIN Console_Versions on game_version = item_ID
INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID;

SELECT title, name FROM Games INNER JOIN Console_Versions ON game_ID = game INNER JOIN Consoles ON console = console_ID;

SELECT first_name, last_name FROM Customers INNER JOIN Rentals ON customer_ID = customer;

SELECT customer_id FROM Customers WHERE first_name = [:first_name] AND last_name = [:last_name];

INSERT INTO Rentals (customer, rent_date, paid) VALUES (%s,%s,%s);

SELECT item_ID FROM Console_Versions INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID WHERE title = %s AND name = %s % (title, name)

SELECT rental_ID FROM Rentals INNER JOIN Customers ON customer = customer_ID WHERE first_name = %s AND last_name = %s % (first_name, last_name)

INSERT INTO Game_Rentals (game_version, rental) VALUES (%s, %s)

DELETE FROM Game_Rentals WHERE game_version = %s AND rental = %s % (gv_id, re_id)

DELETE FROM Rentals WHERE rental_ID = %s

SELECT first_name, last_name, rental_ID, rent_date, paid FROM Rentals INNER JOIN Customers ON customer = customer_ID WHERE rental_id = %s % (r_id)

UPDATE Rentals SET customer = %s, rent_date = %s, paid = %s WHERE rental_id = %s

SELECT customer_ID, first_name, last_name, street, city, state, zip, phone, email, DATE_FORMAT(birthday, '%%b %%e %%Y') as birthday FROM Customers;

SELECT customer, rental, game_version, title, name, DATE_FORMAT(rent_date, '%%b %%e %%Y') AS rent_date, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') AS due,
DATE_FORMAT(paid, '%%b %%e %%Y') AS paid, first_name, last_name FROM Games INNER JOIN Console_Versions ON game_ID = game
INNER JOIN Consoles ON console = console_ID INNER JOIN Game_Rentals ON item_ID = game_version
INNER JOIN Rentals ON rental = rental_ID INNER JOIN Customers ON customer = customer_ID;

INSERT INTO Customers (first_name, last_name, street, city, state, zip, phone, email, birthday) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);

SELECT first_name, last_name, street, city, state, zip, phone, email, birthday, customer_id FROM Customers WHERE [:conditions];

DELETE FROM Customers WHERE customer_ID = %s

SELECT * FROM Customers WHERE customer_ID = %s % (cu_id)

UPDATE Customers SET first_name = %s, last_name = %s, street = %s, city = %s, state = %s, zip = %s, phone = %s, email = %s, birthday = %s WHERE customer_ID = %s